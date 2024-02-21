import pandas as pd
from transform_staff_table import transform_staff_table


def test_transform_transaction_table():
    pqt_file = './test/parquet_test_file/staff.pqt'

    df = pd.read_parquet(pqt_file, engine="pyarrow")

    ts = pd.Timestamp("2022-11-03T14:20:51.563")
    date = ts.date()
    time = ts.time()

    data = [
        [
            1,
            "Jeremie",
            "Franey",
            "jeremie.franey@terrifictotes.com",
            "Purchasing",
            "Manchester",
            date,
            time,
            1
        ]
    ]
    expected_df = pd.DataFrame(
        data,
        columns=[
            "staff_id",
            "first_name",
            "last_name",
            "email_address",
            "department_name",
            "location",
            "last_updated_date",
            "last_updated_time",
            "staff_record_id"
        ]
    )
    transformed_df = transform_staff_table(df)

    expected_df = expected_df.astype(
        {col: 'int32' for col in expected_df.select_dtypes('int64').columns})

    for column, series in transformed_df.items():
        assert transformed_df[column][0] == expected_df[column][0]
