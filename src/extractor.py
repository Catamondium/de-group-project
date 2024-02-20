import pandas as pd
import logging
from os import environ
from datetime import datetime
import pg8000.native as pg
from boto3 import client
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel("INFO")

# anticipated table structure

TABLES = [
    "currency",
    "payment",
    "department",
    "transaction",
    "design",
    "address",
    "staff",
    "counterparty",
    "purchase_order",
    "payment_type",
    "sales_order",
]


def extract(client, conn: pg.Connection, bucket, table, time, since):
    """
    Extracts data from a PostgreSQL database table
    based on the specified time and uploads it to
    an S3 bucket in Parquet format.

    Args:
        client (boto3.client): An instance of the
        Boto3 S3 client.
        conn (pg.Connection): A connection object
        representing the connection to the PostgreSQL
        database.
        bucket (str): The name of the S3 bucket where
        the data will be uploaded.
        table (str): The name of the PostgreSQL
        database table to extract data from.
        time (datetime.datetime): The timestamp representing
        the time from which data should be extracted.

    Returns:
        None

    """
    logger.info(f"extracting {table}")

    if since is not None:
        sql = f"""
            SELECT *
            FROM {pg.identifier(table)}
            WHERE last_updated >= {pg.literal(since)}
            """
    else:
        sql = f"""
            SELECT *
            FROM {pg.identifier(table)}
            """

    rows = conn.run(sql)
    if len(rows) > 0:
        timestring = time.strftime("%Y-%m-%dT%H:%M:%S")

        data = rows_to_dict(rows, conn.columns)
        df = pd.DataFrame(data=data)
        key = f"{timestring}/{table}.pqt"
        logger.info(f"output key is {key}")
        upload_parquet(client, bucket, key, df)


def lambda_handler(event, context):
    """
    Handles the Lambda event and extracts data
    from PostgreSQL tables to upload to an S3
    bucket in Parquet format.

    Args:
        event (dict): The event data passed
        to the Lambda function.
        context (LambdaContext): The runtime
        information of the Lambda function.

    Returns:
        None: The function does not return a
        specific value. It performs data extraction
        and upload tasks without explicit return data.
    """
    try:
        time = datetime.fromisoformat(event["time"])
        username = environ.get("PGUSER", "testing")
        password = environ.get("PGPASSWORD", "testing")
        host = environ.get("PGHOST", "testing")
        port = environ.get("PGPORT", "5432")
        database = environ.get("PGDATABASE")
        connection = pg.Connection(
            username, password=password, host=host,
            port=port, database=database
        )

        s3 = client("s3")
        bucket = environ.get("S3_EXTRACT_BUCKET", "ingestion")

        since = get_last_updated_time(s3)

        # query to dynamically retrieve all valid tables

        rows = connection.run(
            r"""
                    SELECT tablename
                    FROM pg_catalog.pg_tables
                    WHERE schemaname != 'pg_catalog'
                    AND schemaname != 'information_schema'
                    AND tablename NOT LIKE '\_%';
                    """
        )

        assert rows is not None

        tables = [item[0] for item in rows]
        for table in tables:
            extract(s3, connection, bucket, table, time, since)

        set_last_updated_time(s3, datetime.now())

    except Exception as e:
        logger.error(e)


def upload_parquet(client, bucket, key, data):
    """
    Uploads a Pandas DataFrame as a Parquet file
    to an S3 bucket.

    Args:
        client (boto3.client): An S3 client object
        for interacting with AWS S3.
        bucket (str): The name of the S3 bucket
        to upload the Parquet file to.
        key (str): The key (object name) to use
        for the Parquet file within the S3 bucket.
        data (pd.DataFrame): The Pandas DataFrame
        to be uploaded as a Parquet file.

    Returns:
        None: The function does not return a specific value.
        It performs the upload operation directly.
    """
    data.to_parquet(path="/tmp/output.parquet")
    client.upload_file(Bucket=bucket, Key=key, Filename="/tmp/output.parquet")


def rows_to_dict(items, columns):
    """
    Converts rows fetched from a PostgreSQL query
    to a list of dictionaries, where each dictionary
    represents a row with column names as keys.

    Args:
        items (list): A list of lists, where each inner
        list represents a row of data.
        columns (list): A list of dictionaries containing
        information about database columns.

    Returns:
        list: A list of dictionaries, where each
        dictionary represents a row with column names
        as keys and corresponding values.
    """
    accumulator = []
    indices = [col["name"] for col in columns]
    for item in items:
        pairs = [(indices[i], value) for i, value in enumerate(item)]
        accumulator.append(dict(pairs))
    return accumulator


def get_last_updated_time(s3):
    bucket = environ.get("S3_CONTROL_BUCKET", "control_bucket")

    try:
        content = s3.get_object(
            Bucket=bucket, Key="last_successful_extraction.txt")
        last_updated_time = content["Body"].read().decode("utf-8").strip()
        logger.info("LAST UPDATED present")

        return datetime.fromtimestamp(float(last_updated_time))
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            logger.warning(f"No such key error: {e}")
            return None
        else:
            raise e


def set_last_updated_time(s3, current_time: datetime):
    bucket = environ.get("S3_CONTROL_BUCKET", "control_bucket")
    try:
        s3.put_object(
            Bucket=bucket,
            Key="last_successful_extraction.txt",
            Body=str(current_time.timestamp())
        )
        # print("time successfully written")
    except Exception as e:
        logger.error(f"Error writing data to S3: {e}")
