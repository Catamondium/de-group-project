import pandas as pd
import logging
from os import environ
import pg8000.native as pg
from boto3 import client

logger = logging.getLogger()
logger.setLevel("INFO")

# anticipated table structure
TABLES = ["currency",
          "payment",
          "department",
          "transaction",
          "design",
          "address",
          "staff",
          "counterparty",
          "purchase_order",
          "payment_type",
          "sales_order"]


def extract(client, conn: pg.Connection, bucket, table, time):
    rows = conn.run(f"SELECT * FROM {table}")
    data = rows_to_dict(rows, conn.columns)
    print(data)
    df = pd.DataFrame(data=data)
    key = f"{time.isoformat()}/{table}.pqt"
    logger.info(f'output key is {key}')
    upload_parquet(client, bucket, key, df)


def lambda_handler(event, context):
    try:
        time = event['time']

        username = environ.get('PGUSER', 'testing')
        password = environ.get('PGPASSWORD', 'testing')
        host = environ.get('PGHOST', 'testing')
        port = environ.get('PGPORT', '5432')
        database = environ.get('PGDATABASE')
        connection = pg.Connection(
            username, password=password,
            host=host, port=port,
            database=database)

        s3 = client('s3')
        bucket = environ.get('S3_EXTRACT_BUCKET', 'ingestion')

        # query to dynamically retrieve all valid tables
        rows = connection.run(r"""
                    SELECT tablename
                    FROM pg_catalog.pg_tables
                    WHERE schemaname != 'pg_catalog'
                    AND schemaname != 'information_schema'
                    AND tablename NOT LIKE '\_%';
                    """)

        assert rows is not None

        print(rows)

        tables = [item[0] for item in rows]

        for table in tables:
            extract(s3, connection, bucket, table, time)
    except Exception as e:
        logger.error(e)


def upload_parquet(client, bucket, key, data):
    data.to_parquet(path="/tmp/output.parquet")
    client.upload_file(
        Bucket=bucket, Key=key, Filename="/tmp/output.parquet")


def rows_to_dict(items, columns):
    accumulator = []
    indices = [col['name'] for col in columns]
    for item in items:
        pairs = [(indices[i], value) for i, value in enumerate(item)]
        accumulator.append(dict(pairs))
    return accumulator