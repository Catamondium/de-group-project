import pandas as pd
import logging
from os import environ
from datetime import datetime
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
    logger.info(f'extracting {table}')
    last_updated = environ.get("PG_LAST_UPDATED", None)
    sql = f"SELECT * FROM {table} WHERE created_at > to_timestamp('{last_updated}', 'YYYY-MM-DD HH24:MI:SS') OR last_updated > to_timestamp('{last_updated}', 'YYYY-MM-DD HH24:MI:SS')"
    rows = conn.run(sql)
    if len(rows) > 0: 
        data = rows_to_dict(rows, conn.columns)
        df = pd.DataFrame(data=data)
        key = f"{time.isoformat()}/{table}.pqt"
        logger.info(f'output key is {key}')
        upload_parquet(client, bucket, key, df)


def lambda_handler(event, context):
    try:
        time = datetime.strptime(event['time'],"%Y-%m-%dT%H:%M:%SZ")
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


        tables = [item[0] for item in rows]

        for table in tables:
            extract(s3, connection, bucket, table, time)
        environ["PG_LAST_UPDATED"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        logger.info("an error has occurred")
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
