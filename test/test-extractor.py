from extractor import lambda_handler, rows_to_dict, upload_parquet, extract
from moto import mock_aws
import pandas as pd
from unittest.mock import Mock, patch
import boto3
from datetime import datetime
from configparser import ConfigParser
import pytest
from io import BytesIO
import os
from sample_datasets import sample_dataset


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
def mockdb_creds():
    """Mocked AWS Credentials for moto."""

    config = ConfigParser()
    config.read('.env.ini')
    section = config['DEFAULT']

    os.environ['PGUSER'] = section['PGUSER']
    os.environ['PGPASSWORD'] = section['PGPASSWORD']
    os.environ['PGHOST'] = "127.0.0.1"
    os.environ['PGDATABASE'] = "totesys_test_subset"


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

# extract()
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

    df = pd.DataFrame(data=[{'a': 1, 'b': 2, 'c': 'AAA'},
                            {'a': 4, 'b': 5, 'c': 'BBB'}])

    key = f"{datestring}/{table}.pqt"

    extract(client, conn, 'ingestion', table, time)

    upload.assert_called_with(client, 'ingestion', key, SAME_DF(df))


@patch("extractor.upload_parquet")
def test_extract_with_mod_queries(upload):
    client = 's3'
    datestring = "2024-02-13T10:45:18"

    os.environ['S3_EXTRACT_BUCKET'] = 'ingestion'

    conn = Mock()
    conn.run.return_value = [[1, 2, 'AAA'], [4, 5, 'BBB']]
    conn.columns = [{'name': 'a'}, {'name': 'b'}, {'name': 'c'}]
    table = 'design'
    time = datetime.fromisoformat(datestring)

    df = pd.DataFrame(data=[{'a': 1, 'b': 2, 'c': 'AAA'},
                            {'a': 4, 'b': 5, 'c': 'BBB'}])

    key = f"{datestring}/{table}.pqt"

    extract(client, conn, 'ingestion', table, time)

    upload.assert_called_with(client, 'ingestion', key, SAME_DF(df))

@patch("extractor.upload_parquet")
def test_extract_with_mod_queries_plus_last_updated_time(upload):
    client = 's3'
    datestring = "2024-02-13T10:45:18"

    os.environ['S3_EXTRACT_BUCKET'] = 'ingestion'

    conn = Mock()
    conn.run.return_value = [[1, 2, 'AAA'], [4, 5, 'BBB']]
    conn.columns = [{'name': 'a'}, {'name': 'b'}, {'name': 'c'}]
    table = 'design'
    time = datetime.fromisoformat(datestring)

    df = pd.DataFrame(data=[{'a': 1, 'b': 2, 'c': 'AAA'},
                            {'a': 4, 'b': 5, 'c': 'BBB'}])

    key = f"{datestring}/{table}.pqt"

    extract(client, conn, 'ingestion', table, time)

    upload.assert_called_with(client, 'ingestion', key, SAME_DF(df))



@mock_aws
@patch('extractor.client')
@patch("extractor.extract")
@patch("extractor.get_last_updated_time")
@patch("extractor.pg.Connection")
def test_lambda_handler(conn, get_last_updated_time, MockExtract, client):
    time = datetime.fromisoformat("2024-02-13T10:45:18+0000")
    connMock = Mock()
    get_last_updated_time.return_value = "2024-01-01 00:00:00.000000"
    event = {
        'time': time
    }
    context = ''

    client.return_value = 's3'
    conn.return_value = connMock
    connMock.run.return_value = [['example_table']]

    lambda_handler(event, context)

    MockExtract.assert_called_with(
        's3', connMock, 'ingestion', 'example_table', time, "2024-01-01 00:00:00.000000")


@mock_aws
def test_integrate(s3, mockdb_creds):
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
    event = {'time': datetime.fromisoformat("2024-02-13T10:45:18")}

    # ACT
    s3.create_bucket(
        Bucket='ingestion',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'})

    lambda_handler(event, '')

    objects = s3.list_objects_v2(Bucket='ingestion')
    files = [file['Key'] for file in objects['Contents']]

    assert len(files) == 11

    for table in TABLES:
        expected_file_name = f'2024-02-13T10:45:18/{table}.pqt'
        assert expected_file_name in files

        expected_table = sample_dataset[table]
        # print(expected_table[0], table, '-------------------------------')

        resp = s3.get_object(Bucket='ingestion',
                             Key=f"2024-02-13T10:45:18/{table}.pqt")
        df = pd.read_parquet(BytesIO(resp['Body'].read()))
        existing_table = df.to_records()

        for i, row in enumerate(existing_table):
            assert len(row) == len(expected_table[i]) + 1
