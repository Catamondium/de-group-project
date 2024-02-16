import pandas as pd
import logging
from os import environ
import pg8000.native as pg
from boto3 import client
from extractor_queries_dict import get_query  # ,TABLES
from datetime import datetime

logger = logging.getLogger()
logger.setLevel("INFO")


def extract(
    client, conn: pg.Connection, bucket, table, time, last_successful_update_time=None
):

    # todo
    if last_successful_update_time is None:
        query = f"SELECT * FROM {table}"
    else:
        query = get_query(table, last_successful_update_time)

    # print(query, "::::::::::::::::::::::::::::::::")
    rows = conn.run(query)

    data = rows_to_dict(rows, conn.columns)
    if len(data) > 0:
        print(data[0], "<<<<<<<<<<<<<<<<<")
        df = pd.DataFrame(data=data)
        key = f"{time.isoformat()}/{table}.pqt"
        logger.info(f"output key is {key}")
        upload_parquet(client, bucket, key, df)
    else:
        print(f"no new data in {table}")
    return data


def lambda_handler(event, context):
    try:

        time = datetime.strptime(event["time"], "%Y-%m-%dT%H:%M:%SZ")
        username = environ.get("PGUSER", "testing")
        password = environ.get("PGPASSWORD", "testing")
        host = environ.get("PGHOST", "testing")
        port = environ.get("PGPORT", "5432")
        database = environ.get("PGDATABASE")
        connection = pg.Connection(
            username, password=password, host=host, port=port, database=database
        )

        last_updated_time = get_last_updated_time()
        # todo: add error handler if last_updated_time = None ???

        s3 = client("s3")
        bucket = environ.get("S3_EXTRACT_BUCKET", "ingestion")

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

        # assert rows is not None

        tables = [item[0] for item in rows]

        for table in tables:
            extract(s3, connection, bucket, table, time, last_updated_time)

        write_current_time(time)

    except Exception as e:
        logger.error(e)


def upload_parquet(client, bucket, key, data):
    data.to_parquet(path="/tmp/output.parquet")
    client.upload_file(Bucket=bucket, Key=key, Filename="/tmp/output.parquet")


def rows_to_dict(items, columns):
    accumulator = []
    indices = [col["name"] for col in columns]
    for item in items:
        pairs = [(indices[i], value) for i, value in enumerate(item)]
        accumulator.append(dict(pairs))
    return accumulator


def get_last_updated_time():
    s3 = client("s3")
    bucket = environ.get("S3_CONTROL_BUCKET", "control_bucket")

    try:
        content = s3.get_object(Bucket=bucket, Key="last_successful_extraction.txt")
        last_updated_time = content["Body"].read().decode("utf-8").strip()
        return last_updated_time
    except Exception as e:
        print(f"Error retrieving data from S3: {e}")
        #
        return None


def write_current_time(current_time):
    s3 = client("s3")
    bucket = environ.get("S3_CONTROL_BUCKET", "control_bucket")

    try:
        s3.put_object(
            Bucket=bucket, Key="last_successful_extraction.txt", Body=str(current_time)
        )
        # print("time successfully written")
    except Exception as e:
        print(f"Error writing data to S3: {e}")
