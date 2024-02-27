import boto3
import logging
import pg8000.native as pg

# import pandas as pd
# from io import BytesIO
import awswrangler as wr
from os import environ
import numpy as np

s3 = boto3.client("s3")
logger = logging.getLogger()
logger.setLevel("INFO")


table_relations = {
    "currency": ("dim_currency", "currency_record_id"),
    "payment": ("fact_payment", "payment_record_id"),
    "transaction": ("dim_transaction", "transaction_record_id"),
    "design": ("dim_design", "design_record_id"),
    "address": ("dim_location", "location_record_id"),
    "staff": ("dim_staff", "staff_record_id"),
    "counterparty": ("dim_counterparty", "counterparty_record_id"),
    "purchase_order": ("fact_purchase_order", "purchase_record_id"),
    "payment_type": ("dim_payment_type", "payment_type_record_id"),
    "sales_order": ("fact_sales_order", "sales_record_id"),
}


def lambda_handler(event, context):
    try:
        # get bucket
        bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        file_key = event["Records"][0]["s3"]["object"]["key"].replace(
            "%3A", ":"
        )
        table_name = get_table_name(file_key)
        # get dataframe
        logger.info(f"📂 Processing file {file_key} from bucket {bucket_name}")
        df = get_df_from_parquet(file_key, bucket_name)
        # get db_table_name and primary_key
        table_name, primary_key = table_relations[table_name]
        # create query template for specific table fill with placeholders
        sql_query_template = create_query(table_name, primary_key, df)
        # insert
        logger.info(f"🚀 Executing SQL query on table {table_name}")
        df_insertion(sql_query_template, df, table_name)
        logger.info(f"✅ Successfully inserted data into {table_name}")
        return "Ok"
    except Exception as e:
        logger.error(f"❌ Failed to process file: {str(e)}")


def create_query(table_name, primary_key, df):

    columns = list(df.columns)
    placeholders = ", ".join([f":{col}" for col in columns])
    assignments = ", ".join(
        [f"{col} = EXCLUDED.{col}" for col in columns if col != primary_key]
    )

    sql_query_template = f"""
    INSERT INTO {table_name} ({', '.join(columns)})
    VALUES ({placeholders})
    ON CONFLICT ({primary_key})
    DO UPDATE SET {assignments};
    """
    if table_name == "dim_transaction":
        sql_query_template = sql_query_template.replace(
            ":sales_order_id", "nullif(:sales_order_id, -1)"
        )
        sql_query_template = sql_query_template.replace(
            ":purchase_order_id", "nullif(:purchase_order_id, -1)"
        )
    return sql_query_template


def get_df_from_parquet(key, bucket_name):
    pqt_object = [f"s3://{bucket_name}/{key}"]
    df = wr.s3.read_parquet(path=pqt_object)
    return df


def get_table_name(key):
    return key[:-4].split("/")[1]


def df_insertion(query, df, table_name):
    try:
        username = environ.get("PGUSER2", "testing")
        password = environ.get("PGPASSWORD2", "testing")
        host = environ.get("PGHOST2", "testing")
        port = environ.get("PGPORT2", "5432")
        database = environ.get("PGDATABASE2")
        if table_name == "dim_transaction":
            print("got to here")
            df = df.replace({np.nan: -1})
            df = df.astype(
                {col: "int64" for col in df.select_dtypes("float64").columns}
            )
        with pg.Connection(
            username,
            password=password,
            host=host,
            port=port,
            database=database,
        ) as con:
            ps = con.prepare(query)
            for _, row in df.iterrows():
                logger.info(str(row.to_dict()))
                ps.run(**row.to_dict())
            #
        return f"{table_name} Loaded ✅️🤘️"
    except Exception as e:
        logger.error(f"❗ Failed to insert data into {table_name}: {str(e)}")
