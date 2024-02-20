import pandas as pd
from transform_transaction_table import transform_transaction_table


def test_transform_transaction_table():
    pqt_file = './test/parquet_test_file/transaction.pqt'

    df = pd.read_parquet(pqt_file, engine="pyarrow")

    ts = pd.Timestamp("2022-11-03T14:20:52.186")
    date = ts.date()
    time = ts.time()

    data = [
        [
            1,
            "PURCHASE",
            None,
            2,
            date,
            time,
            1
        ]
    ]
    expected_df = pd.DataFrame(
        data,
        columns=[
            "transaction_id",
            "transaction_type",
            "sales_order_id",
            "purchase_order_id",
            "last_updated_date",
            "last_updated_time",
            "transaction_record_id"
        ]
    )
    transformed_df = transform_transaction_table(df)
    expected_df = expected_df.astype(
        {col: 'int32' for col in expected_df.select_dtypes('int64').columns})

    assert transformed_df.equals(expected_df)
