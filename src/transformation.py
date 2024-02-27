import logging
from urllib.request import urlopen
from json import loads
import os
import boto3
import pandas as pd
import awswrangler as wr
import botocore

s3 = boto3.client("s3")
logger = logging.getLogger()
logger.setLevel("INFO")


def lambda_handler(event, context):
    try:
        bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        file_key = event["Records"][0]["s3"]["object"]["key"].replace(
            "%3A", ":"
        )
        table_name = get_table_name(file_key)

        if table_name in list(tables_transformation_templates.keys()):
            # read the file - return dataframe
            df = get_df_from_parquet(file_key, bucket_name)
            # transform df due to template
            new_df = tables_transformation_templates[table_name](df)
            upload_parquet(
                s3,
                os.environ.get(
                    "S3_TRANSFORMATION_BUCKET", "test_transform_bucket"
                ),
                file_key,
                new_df,
            )

    except botocore.exceptions.ClientError as e:
        logger.error(
            """Error accessing S3 name: %s, object key: %s
                     Response error: %s, Message: %s""",
            bucket_name,
            file_key,
            e.response["Error"]["Code"],
            e.response["Error"]["Message"],
        )
    except Exception as e:
        logger.error(e)
        raise e


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


def split_time(df, col_name, new_date_col_name, new_time_col_name):
    df[col_name] = pd.to_datetime(df[col_name])

    # split
    df[new_date_col_name] = df[col_name].dt.date
    df[new_time_col_name] = df[col_name].dt.time

    return df


def payment_transformation(df):
    # DUPLICATE payment_id
    df["payment_record_id"] = df["payment_id"]
    # created_at - SPLIT
    df = split_time(df, "created_at", "created_date", "created_time")
    # last_updated - SPLIT
    df = split_time(
        df, "last_updated", "last_updated_date", "last_updated_time"
    )
    # transaction_id - RENAME TO transaction_record_id
    df.rename(
        columns={"transaction_id": "transaction_record_id"}, inplace=True
    )
    # counterparty_id - RENAME TO counterparty_record_id
    df.rename(
        columns={"counterparty_id": "counterparty_record_id"}, inplace=True
    )
    # payment_amount - OK
    # currency_id - RENAME TO currency_record_id
    df.rename(columns={"currency_id": "currency_record_id"}, inplace=True)
    # payment_type_id - RENAME TO payment_type_record_id
    df.rename(
        columns={"payment_type_id": "payment_type_record_id"}, inplace=True
    )
    # paid - OK
    # payment_date - OK
    # company_ac_number - DELETE
    df.drop("company_ac_number", axis=1, inplace=True)
    # counterparty_ac_number - DELETE
    df.drop("counterparty_ac_number", axis=1, inplace=True)
    df.drop("created_at", axis=1, inplace=True)
    df.drop("last_updated", axis=1, inplace=True)
    return df


def purchase_order_transformation(df):
    # purchase_order_id RENAME  purchase_record_id
    # AND DUPLICATE
    df["purchase_record_id"] = df["purchase_order_id"]
    # created_at SPLIT TO created_date, created_time
    df = split_time(df, "created_at", "created_date", "created_time")
    # last_updated SPLIT TO last_updated_date, last_updated_time
    df = split_time(
        df, "last_updated", "last_updated_date", "last_updated_time"
    )
    # staff_id RENAME TO staff_record_id
    df.rename(columns={"staff_id": "staff_record_id"}, inplace=True)
    # counterparty_id RENAME TO counterparty_record_id
    df.rename(
        columns={"counterparty_id": "counterparty_record_id"}, inplace=True
    )
    # item_code - OK
    # item_quantity - OK
    # item_unit_price - OK
    # currency_id -RENAME TO currency_record_id
    df.rename(columns={"currency_id": "currency_record_id"}, inplace=True)
    # agreed_delivery_date - OK
    # agreed_payment_date - OK
    # agreed_delivery_location_id - OK

    df.drop("created_at", axis=1, inplace=True)
    df.drop("last_updated", axis=1, inplace=True)

    # ✅️ result df should contain columns:
    # purchase_record_id
    # purchase_order_id
    # created_date
    # created_time
    # last_updated_date
    # last_updated_time
    # staff_record_id
    # counterparty_record_id
    # item_code
    # item_quantity
    # item_unit_price
    # currency_record_id
    # agreed_delivery_date
    # agreed_payment_date
    # agreed_delivery_location_id

    return df


def sales_order_transformation(df):
    # OLD
    # sales_order_id DUPL sales_record_id, sales_order_id
    df["sales_record_id"] = df["sales_order_id"]
    # created_at SPLIT TO created_date, created_time
    df = split_time(df, "created_at", "created_date", "created_time")
    # last_updated SPLIT TO last_updated_date, last_updated_time
    df = split_time(
        df, "last_updated", "last_updated_date", "last_updated_time"
    )
    # design_id RENAME design_record_id
    # staff_id RENAME sales_staff_id
    # counterparty_id RENAME counterparty_record_id
    # currency_id RENAME currency_record_id
    df.rename(
        columns={
            "design_id": "design_record_id",
            "staff_id": "sales_staff_id",
            "counterparty_id": "counterparty_record_id",
            "currency_id": "currency_record_id",
        },
        inplace=True,
    )
    df.drop("created_at", axis=1, inplace=True)
    df.drop("last_updated", axis=1, inplace=True)
    # do nothing:
    # agreed_delivery_date
    # agreed_payment_date
    # agreed_delivery_location_id
    # units_sold
    # unit_price

    # result dataframe should contain columns:
    # sales_record_id
    # sales_order_id
    # created_date
    # created_time
    # last_updated_date
    # last_updated_time
    # design_record_id
    # sales_staff_id
    # counterparty_record_id
    # currency_record_id
    # units_sold
    # unit_price
    # agreed_payment_date
    # agreed_delivery_date
    # agreed_delivery_location_id

    return df


def transform_address_table(df):
    df["last_updated_date"] = df["last_updated"].dt.date
    df["last_updated_time"] = df["last_updated"].dt.time
    df["location_record_id"] = df["address_id"]

    df.drop(
        columns=[
            "last_updated",
            "created_at",
        ],
        inplace=True,
    )

    return df


def transform_counterparty_table(df):

    df["last_updated_date"] = df["last_updated"].dt.date
    df["last_updated_time"] = df["last_updated"].dt.time

    df["counterparty_record_id"] = df["counterparty_id"]

    rename_dict = {
        "address_line_1": "counterparty_legal_address_line_1",
        "address_line_2": "counterparty_legal_address_line_2",
        "district": "counterparty_legal_district",
        "city": "counterparty_legal_city",
        "postal_code": "counterparty_legal_postal_code",
        "country": "counterparty_legal_country",
        "phone": "counterparty_legal_phone_number",
    }
    df.rename(columns=rename_dict, inplace=True)

    df.drop(
        columns=[
            "last_updated",
            "created_at",
            "legal_address_id",
            "commercial_contact",
            "delivery_contact",
        ],
        inplace=True,
    )
    return df


def transform_currency(df):
    url = "https://raw.githubusercontent.com/umpirsky/currency-list/master/data/en_GB/currency.json"  # noqa
    response = urlopen(url)

    json_raw = response.read().decode("utf-8")
    currencies = loads(json_raw)

    curr_ls = [
        {
            "currency_code": k,
            "currency_name": v,
        }
        for k, v in currencies.items()
    ]

    currency_df = pd.DataFrame(data=curr_ls)

    df = df.merge(currency_df, how="left", on="currency_code", validate="m:1")

    df["last_updated_date"] = df["last_updated"].dt.date
    df["last_updated_time"] = df["last_updated"].dt.time
    df["currency_record_id"] = df["currency_id"]
    df.drop(columns=["last_updated", "created_at"], inplace=True)

    return df


def transform_design_table(df):
    df["last_updated_date"] = df["last_updated"].dt.date
    df["last_updated_time"] = df["last_updated"].dt.time
    df["design_record_id"] = df["design_id"]
    df.drop(columns=["last_updated", "created_at"], inplace=True)

    return df


def transform_payment_type_table(df):
    df["last_updated_date"] = df["last_updated"].dt.date
    df["last_updated_time"] = df["last_updated"].dt.time
    df["payment_type_record_id"] = df["payment_type_id"]
    df["payment_record_id"] = df["payment_type_id"]
    df.drop(
        columns=["last_updated", "created_at", "payment_type_id"], inplace=True
    )
    return df


def transform_staff_table(df):
    df["last_updated_date"] = df["last_updated"].dt.date
    df["last_updated_time"] = df["last_updated"].dt.time

    df["staff_record_id"] = df["staff_id"]

    df.drop(
        columns=["last_updated", "created_at", "department_id"], inplace=True
    )
    return df


def transform_transaction_table(df):
    df["last_updated_date"] = df["last_updated"].dt.date
    df["last_updated_time"] = df["last_updated"].dt.time
    df["transaction_record_id"] = df["transaction_id"]
    df.drop(
        columns=[
            "last_updated",
            "created_at",
        ],
        inplace=True,
    )

    return df


tables_transformation_templates = {
    "payment": payment_transformation,
    "purchase_order": purchase_order_transformation,
    "sales_order": sales_order_transformation,
    "address": transform_address_table,
    "counterparty": transform_counterparty_table,
    "currency": transform_currency,
    "design": transform_design_table,
    "payment_type": transform_payment_type_table,
    "staff": transform_staff_table,
    "transaction": transform_transaction_table,
}
