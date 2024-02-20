import pandas as pd
from transform_payment_type_table import transform_payment_type_table


def test_transform_payment_type_table():
    pqt_file = './test/parquet_test_file/payment_type.pqt'

    df = pd.read_parquet(pqt_file, engine="pyarrow")
    ts = pd.Timestamp("2022-11-03T14:20:49.962")
    date = ts.date()
    time = ts.time()

    data = [
        [
            "SALES_RECEIPT",
            date,
            time,
            1,
            1,
        ]
    ]
    expected_df = pd.DataFrame(
        data,
        columns=[
            "payment_type_name",
            "last_updated_date",
            "last_updated_time",
            "payment_type_record_id",
            "payment_record_id",
        ]
    )
    transformed_df = transform_payment_type_table(df)
    expected_df = expected_df.astype(
        {col: 'int32' for col in expected_df.select_dtypes('int64').columns})

    assert transformed_df.equals(expected_df)
