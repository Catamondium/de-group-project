from extractor import extract
from moto import mock_aws
from unittest.mock import patch  # , Mock
import boto3
from datetime import datetime
from configparser import ConfigParser
import pytest
import os
import pg8000.native as pg


@pytest.fixture(scope='function')
def mockdb_creds():
    """sd."""

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


@pytest.fixture(scope='function')
def db_connection(mockdb_creds):
    """ connect to db """
    conn = pg.Connection(
        user=os.getenv('PGUSER'),
        password=os.getenv('PGPASSWORD'),
        host=os.getenv('PGHOST'),
        database=os.getenv('PGDATABASE')
    )
    yield conn
    conn.close()


def test_connection_to_test_db(db_connection):
    """ test connection to test DB """
    try:
        conn = db_connection
        cursor = conn.run("SELECT 1")

        assert cursor[0][0] == 1, "Cant connect to test DB."
    except Exception as e:
        pytest.fail(f"Connection error: {e}")


@patch("extractor.upload_parquet")
def test_extract_query_design_no_timestamp(mock_upload_parquet, db_connection):
    client = 's3'
    bucket = 'ingestion'
    table = 'design'
    time = datetime.fromisoformat("2024-02-13T10:45:18")

    data = extract(client, db_connection, bucket, table, time)

    mock_upload_parquet.assert_called_once()
    assert len(data) == 10


@patch("extractor.upload_parquet")
def test_extract_query_design_with_timestamp(mock_upload_parquet,
                                             db_connection):
    client = 's3'
    bucket = 'ingestion'
    table = 'design'
    time = datetime.fromisoformat("2024-02-13T10:45:18")

    data = extract(client,
                   db_connection,
                   bucket, table, time,
                   '2024-01-01 12:00:00.000')

    mock_upload_parquet.assert_called_once()
    assert len(data) == 10
