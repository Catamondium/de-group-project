import boto3
import logging

# import pandas as pd
# from io import BytesIO
import awswrangler as wr
import os
from transformation_dictionary import tables_transformation_templates

s3 = boto3.client("s3")
logger = logging.getLogger()
logger.setLevel("INFO")


def lambda_handler(event, context):
    try:
        bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        file_key = event["Records"][0]["s3"]["object"]["key"]
        table_name = get_table_name(file_key)

        if table_name in list(tables_transformation_templates.keys()):
            # read the file - return dataframe
            df = get_df_from_parquet(file_key, bucket_name)
            # transform df due to template
            new_df = tables_transformation_templates[table_name](df)
            print(new_df, "🧨️-🧨-️🧨-️🧨️-🧨️-🧨️")
            upload_parquet(
                s3, os.environ.get("S3_TRANSFORMATION_BUCKET",
                                   "test_transform_bucket"),
                file_key,
                new_df
            )
            return "Done something"
        # save df to parquet_file
        return "Done nothing"
    except Exception as e:
        logger.error(e)


def get_df_from_parquet(key, bucket_name):
    pqt_object = [f"s3://{bucket_name}/{key}"]
    df = wr.s3.read_parquet(path=pqt_object)
    return df


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


def get_table_name(key):
    return key[:-4].split("/")[1]
