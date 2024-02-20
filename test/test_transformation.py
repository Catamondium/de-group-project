from transformation import lambda_handler
from moto import mock_aws
# import pandas as pd
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
