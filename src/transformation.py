# import boto3
# import pandas as pd
# from io import BytesIO
import awswrangler as wr
import os

# s3 = boto3.client('s3')


def lambda_handler(event, context):
    # bucket_name = event['Records'][0]['s3']['bucket']['name']
    # file_key = event['Records'][0]['s3']['object']['key']

    # read the file - return dataframe
    # df = get_df_from_parquet(file_key)

    # identify template
    # transform "2024-02-02/design.prquet" --> design

    # transform df
    # due to template
    # new_df = tables_transformation_templates[table](df)

    # save df to parquet_file
    return 0


def get_df_from_parquet(key):
    bucket = os.environ["S3_EXTRACT_BUCKET"]
    pqt_object = [f"s3://{bucket}/{key}"]
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
