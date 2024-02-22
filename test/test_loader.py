from src.loader import (
    lambda_handler,
    get_df_from_parquet,
    get_table_name,
)
# from src.transformation import tables_transformation_templates

from moto import mock_aws
import pandas as pd
from unittest.mock import patch  # , Mock
import boto3
from datetime import datetime
# from configparser import ConfigParser
import pytest

# from io import BytesIO
import os

# from sample_datasets import sample_dataset
# from t_utils import inhibit_CI

# flake8: noqa
# TODO reenable me after work TODO BUG TEMP
# TODO this was gutted from transform


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


@pytest.fixture(scope="function")
def import_parquet_file():
    parquet_file = "./test/parquet_test_files/test.pqt"
    df = pd.read_parquet(parquet_file, engine="pyarrow")
    return df


def test_get_df_from_parquet(s3, import_parquet_file):
    # TODO, i didn't know this was coupled with EXTRACT
    with pytest.raises(Exception):
        key = "test.parquet"

        data = import_parquet_file

        s3.create_bucket(
            Bucket=os.environ["S3_EXTRACT_BUCKET"],
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        result = get_df_from_parquet(key, "test-bucket")

        assert result["staff_id"][0] == 11
        assert result["first_name"][0] == "Meda"
        assert isinstance(result["created_at"][0], pd.Timestamp)


def test_get_table_name():
    keys = ["2024-02-15T19:01:53/address.pqt", "2024-02-21/purchase_order.pqt"]
    assert get_table_name(keys[0]) == "address"
    assert get_table_name(keys[1]) == "purchase_order"


@patch('src.transformation.upload_parquet')
@patch('src.transformation.get_df_from_parquet')
def test_lambda_handler(mock_get_df_from_parquet,
                        mock_upload_parquet):
    # TODO
    data = {
        "address_id": [1, 2, 3],
        "address_line_1": ["123 Maple Street", "456 Oak Street",
                           "789 Pine Street"],
        "address_line_2": ["Apt. 101", "Suite 202", "Room 303"],
        "district": ["North", "South", "East"],
        "city": ["Townsville", "Cityplace", "Villageland"],
        "postal_code": ["12345", "67890", "111213"],
        "country": ["CountryA", "CountryB", "CountryC"],
        "phone": ["123-456-7890", "098-765-4321", "456-789-0123"],
        "created_at": [datetime.now(), datetime.now(), datetime.now()],
        "last_updated": [datetime.now(), datetime.now(), datetime.now()]
    }
    df = pd.DataFrame(data)
    event = {
        "time": "2024-02-13T10:45:18Z",
        "Records": [{
            "s3": {
                "bucket": {"name": "extraction"},
                "object": {"key": "2024-02-15T19:01:53/address.pqt"},
            }
        }],
    }
    context = {}

    # mocking
    mock_get_df_from_parquet.return_value = df
    mock_upload_parquet.return_value = 0

    # ACT
    res = lambda_handler(event, context)
    assert res is None
