from transformation import lambda_handler, upload_parquet, get_df_from_parquet
from moto import mock_aws

import pandas as pd
from unittest.mock import patch  # , Mock
import boto3

# from datetime import datetime
# from configparser import ConfigParser
import pytest

# from io import BytesIO
import os

# from sample_datasets import sample_dataset
# from t_utils import inhibit_CI


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""

    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture(scope="function")
def s3(aws_credentials):
    with mock_aws():
        yield boto3.client("s3")


@mock_aws
@patch("extractor.client")
@patch("extractor.extract")
@patch("extractor.pg.Connection")
def test_lambda_handler(conn, MockExtract, client):
    event = {"time": "2024-02-13T10:45:18Z"}
    context = ""

    a = lambda_handler(event, context)
    assert a == 0


@mock_aws
def test_upload_parquet(s3):
    """
    tests upload_parquet functionality
    """
    bucket = "test-bucket"
    key = "test.parquet"

    data = pd.DataFrame([{"a": 1}])

    s3.create_bucket(
        Bucket=bucket,
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )

    upload_parquet(s3, bucket, key, data)

    objects = s3.list_objects_v2(Bucket=bucket)

    files = [file["Key"] for file in objects["Contents"]]

    assert key in files


@pytest.fixture(scope="function")
def import_parquet_file():
    parquet_file = "./test/parquet_test_files/test.pqt"
    df = pd.read_parquet(parquet_file, engine="pyarrow")
    return df


def test_get_df_from_parquet(s3, import_parquet_file):
    os.environ["S3_EXTRACT_BUCKET"] = "test-bucket"
    key = "test.parquet"

    data = import_parquet_file

    s3.create_bucket(
        Bucket=os.environ["S3_EXTRACT_BUCKET"],
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )

    upload_parquet(s3, os.environ["S3_EXTRACT_BUCKET"], key, data)

    result = get_df_from_parquet(key)

    assert result["staff_id"][0] == 11
    assert result["first_name"][0] == "Meda"
    assert isinstance(result["created_at"][0], pd.Timestamp)
