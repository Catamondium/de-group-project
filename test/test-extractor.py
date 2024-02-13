from extractor import lambda_handler, rows_to_dict, upload_parquet, extract
from moto import mock_aws
import pandas as pd
from unittest.mock import Mock, patch
import boto3
from datetime import datetime
import pytest
import os


class SAME_DF:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def __eq__(self, other):
        return isinstance(other, pd.DataFrame) and other.equals(self.df)


class TestRowstoDict:
    def test_empty(self):
        items = []
        columns = []
        expected = []

        actual = rows_to_dict(items, columns)

        assert actual == expected

    def test_single(self):
        items = [[1]]
        columns = [{'name': 'a'}]
        expected = [{'a': 1}]

        actual = rows_to_dict(items, columns)

        assert actual == expected

    def test_multiple(self):
        items = [[1, 2, 'AAA'], [4, 5, 'BBB']]
        columns = [{'name': 'a'}, {'name': 'b'}, {'name': 'c'}]
        expected = [{'a': 1, 'b': 2, 'c': 'AAA'},
                    {'a': 4, 'b': 5, 'c': 'BBB'}]

        actual = rows_to_dict(items, columns)

        assert actual == expected


@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""

    os.environ['AWS_ACCESS_KEY_ID'] = 'test'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'
    os.environ['AWS_SECURITY_TOKEN'] = 'test'
    os.environ['AWS_SESSION_TOKEN'] = 'test'
    os.environ['AWS_DEFAULT_REGION'] = 'eu-west-2'


@pytest.fixture(scope='function')
def s3(aws_credentials):
    with mock_aws():
        yield boto3.client('s3')


@mock_aws
def test_upload_parquet(s3):
    bucket = 'test-bucket'
    key = 'test.parquet'

    data = pd.DataFrame([{'a': 1}])

    s3.create_bucket(
        Bucket=bucket,
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'})

    upload_parquet(s3, bucket, key, data)

    objects = s3.list_objects_v2(Bucket=bucket)

    files = [file['Key'] for file in objects['Contents']]

    assert key in files


@patch("extractor.upload_parquet")
def test_extract(upload):
    client = 's3'
    datestring = "2024-02-13T10:45:18"

    os.environ['S3_EXTRACT_BUCKET'] = 'ingestion'

    conn = Mock()
    conn.run.return_value = [[1, 2, 'AAA'], [4, 5, 'BBB']]
    conn.columns = [{'name': 'a'}, {'name': 'b'}, {'name': 'c'}]
    table = 'cat'
    time = datetime.fromisoformat(datestring)

    df = pd.DataFrame(data=[{'a': 1, 'b': 2, 'c': 'AAA'}, {
                      'a': 4, 'b': 5, 'c': 'BBB'}])

    key = f"{datestring}/{table}.pqt"

    extract(client, conn, 'ingestion', table, time)

    upload.assert_called_with(client, 'ingestion', key, SAME_DF(df))


@mock_aws
@patch('extractor.client')
@patch("extractor.extract")
@patch("extractor.pg.Connection")
def test_lambda_handler(conn, MockExtract, client):
    time = datetime.fromisoformat("2024-02-13T10:45:18+0000")
    connMock = Mock()

    event = {
        'time': time
    }
    context = ''

    client.return_value = 's3'
    conn.return_value = connMock
    connMock.run.return_value = [['example_table']]

    lambda_handler(event, context)

    MockExtract.assert_called_with(
        's3', connMock, 'ingestion', 'example_table', time)
