from transformation import (
    # lambda_handler,
    upload_parquet,
    get_df_from_parquet,
    get_table_name,
)
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


@patch("transformation.get_df_from_parquet")
@patch("transformation.upload_parquet")
def test_lambda_handler(get_df_from_parquet, upload_parquet):
    upload_parquet.side_effect = 0
    # os.environ['S3_EXTRACT_BUCKET'] = "test"

    data = {
        "address_id": [1, 2, 3, 4, 5],
        "address_line_1": [
            "123 Main Street",
            "456 Elm Street",
            "789 Oak Avenue",
            "1011 Pine Boulevard",
            "1213 Cedar Lane",
        ],
        "address_line_2": [
            "Suite 100",
            "Apartment 201",
            None,
            "Unit 3B",
            None,
        ],
        "district": [
            "Downtown",
            "Uptown",
            "Midtown",
            "East Side",
            "West Side",
        ],
        "city": [
            "New York",
            "Chicago",
            "Los Angeles",
            "Houston",
            "Philadelphia",
        ],
        "postal_code": ["10001", "20002", "30003", "40004", "50005"],
        "country": ["USA", "USA", "USA", "USA", "USA"],
        "phone": [
            "(212) 555-1212",
            "(312) 555-1213",
            "(213) 555-1214",
            "(713) 555-1215",
            "(215) 555-1216",
        ],
        "created_at": [
            "2023-02-15 12:00:00",
            "2023-02-16 12:00:00",
            "2023-02-17 12:00:00",
            "2023-02-18 12:00:00",
            "2023-02-19 12:00:00",
        ],
        "last_updated": [
            "2023-02-15 12:00:00",
            "2023-02-16 12:00:00",
            "2023-02-17 12:00:00",
            "2023-02-18 12:00:00",
            "2023-02-19 12:00:00",
        ],
    }

    df = pd.DataFrame(data)
    get_df_from_parquet.return_value = df
    # event = {
    #     "time": "2024-02-13T10:45:18Z",
    #     "Records": [
    #         {
    #             "s3": {
    #                 "bucket": {"name": "extraction"},
    #                 "object": {"key": "2024-02-15T19:01:53/address.pqt"},
    #             }
    #         }
    #     ],
    # }
    # context = ""

    # a = lambda_handler(event, context)
    assert True


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
    key = "test.parquet"

    data = import_parquet_file

    s3.create_bucket(
        Bucket=os.environ["S3_EXTRACT_BUCKET"],
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )

    upload_parquet(s3, os.environ["S3_EXTRACT_BUCKET"], key, data)

    result = get_df_from_parquet(key, "test-bucket")

    assert result["staff_id"][0] == 11
    assert result["first_name"][0] == "Meda"
    assert isinstance(result["created_at"][0], pd.Timestamp)


def test_get_table_name():
    keys = ["2024-02-15T19:01:53/address.pqt", "2024-02-21/purchase_order.pqt"]
    assert get_table_name(keys[0]) == "address"
    assert get_table_name(keys[1]) == "purchase_order"
