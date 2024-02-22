import boto3
import logging

# import pandas as pd
# from io import BytesIO
import awswrangler as wr
import os

s3 = boto3.client("s3")
logger = logging.getLogger()
logger.setLevel("INFO")

# TODO skeleton for terraform
# flake8: noqa
# TODO reenable me after work TODO BUG TEMP


def lambda_handler(event, context):
    try:
        bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        file_key = event["Records"][0]["s3"]["object"]["key"]
        table_name = get_table_name(file_key)

        df = get_df_from_parquet(file_key, bucket_name)
        pass  # TODO
    except Exception as e:
        logger.error(e)


def get_df_from_parquet(key, bucket_name):
    pqt_object = [f"s3://{bucket_name}/{key}"]
    df = wr.s3.read_parquet(path=pqt_object)
    return df


def get_table_name(key):
    return key[:-4].split("/")[1]
