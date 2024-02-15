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


def extract(client,
            conn: pg.Connection,
            bucket,
            table,
            time,
            last_successful_update_time=None):
    # design: [ "sales_order": "desing_id" ]

    # WITH des_ids as (SELECT desing_id
    # FROM sasales_order
    # WHERE last_updated > {last_successful_update_time})
    # SELECT * FROM design WHERE design_id in des_ids

    ##############################################################
    # QUERIES
    # design
    queries = {
        # todo: fix
        "design": f'''
        SELECT * FROM design
        WHERE last_updated > '{last_successful_update_time}'
        UNION
        SELECT d.* FROM design d
        INNER JOIN sales_order so ON d.design_id = so.design_id
        WHERE so.last_updated > '{last_successful_update_time}';''',

        "payment_type": f'''
        SELECT * FROM payment_type
        WHERE last_updated > '{last_successful_update_time}'
        UNION
        SELECT pt.* FROM payment_type pt
        INNER JOIN payment p ON pt.payment_type_id = p.payment_type_id
        WHERE p.last_updated > '{last_successful_update_time}';''',

        "payment": f'''
        SELECT * FROM payment
        WHERE last_updated > '{last_successful_update_time}';''',

        "currency": f'''
        SELECT * FROM currency
        WHERE last_updated >= '{last_successful_update_time}'
        UNION
        SELECT * FROM currency WHERE currency_id in
        (SELECT currency_id
        FROM payment
        WHERE last_updated >= '{last_successful_update_time}')
        UNION
        (SELECT DISTINCT c.* FROM currency c
        INNER JOIN purchase_order po ON c.currency_id = po.currency_id
        INNER JOIN transaction t ON po.purchase_order_id = t.purchase_order_id
        WHERE T.created_at > '{last_successful_update_time}')
        UNION
        (SELECT DISTINCT c.* FROM currency c
        INNER JOIN sales_order co ON c.currency_id = co.currency_id
        INNER JOIN transaction t ON co.sales_order_id = t.sales_order_id
        WHERE T.created_at > '{last_successful_update_time}');''',

        # todo dep
        "department": f'''
        SELECT * FROM department
        WHERE last_updated >= '{last_successful_update_time}';''',

        # todo  transaction
        "transaction": f'''
        SELECT * FROM transaction
        WHERE last_updated >= '{last_successful_update_time}';''',

        # todo addr
        "address": f'''
        SELECT * FROM address
        WHERE last_updated >= '{last_successful_update_time}';''',

        # todo staff
        "staff": f'''
        SELECT * FROM staff
        WHERE last_updated >= '{last_successful_update_time}';''',

        "counterparty": f'''
        SELECT * FROM counterparty
        WHERE last_updated >= '{last_successful_update_time}';''',

        "purchase_order": f'''
        SELECT * FROM purchase_order
        WHERE last_updated >= '{last_successful_update_time}';''',

        "sales_order": f'''
        SELECT * FROM sales_order
        WHERE last_updated >= '{last_successful_update_time}';''',
    }

    if last_successful_update_time is None:
        query = f"SELECT * FROM {table}"
    else:
        query = queries[table]

    # print(query, "::::::::::::::::::::::::::::::::")
    rows = conn.run(query)
    data = rows_to_dict(rows, conn.columns)
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

        last_updated_time = get_last_updated_time()
        # todo: add error handler if last_updated_time = None ???

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

        # assert rows is not None

        tables = [item[0] for item in rows]

        for table in tables:
            extract(s3, connection, bucket, table, time, last_updated_time)

        write_current_time(time)

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


def get_last_updated_time():
    s3 = client('s3')
    bucket = environ.get('S3_CONTROL_BUCKET', 'control_bucket')

    try:
        content = s3.get_object(Bucket=bucket,
                                Key='last_successful_transformation.txt')
        last_updated_time = content['Body'].read().decode('utf-8').strip()
        return last_updated_time
    except Exception as e:
        print(f"Error retrieving data from S3: {e}")
        #
        return None


def write_current_time(current_time):
    s3 = client('s3')
    bucket = environ.get('S3_CONTROL_BUCKET', 'control_bucket')

    try:
        s3.put_object(Bucket=bucket,
                      Key='last_successful_extraction.txt',
                      Body=current_time)
        # print("time successfully written")
    except Exception as e:
        print(f"Error writing data to S3: {e}")
