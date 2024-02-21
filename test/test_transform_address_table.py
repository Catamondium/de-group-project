import pandas as pd
from transform_address_table import transform_address_table


def test_transform_address_table():
    pqt_file = "./test/parquet_test_file/address.pqt"

    df = pd.read_parquet(pqt_file, engine="pyarrow")
    df["postal_code"] = df["postal_code"].astype(str)
    ts = pd.Timestamp("2022-11-03T14:20:49.962")
    date = ts.date()
    time = ts.time()

    data = [
        [
            1,
            "6826 Herzog Via",
            None,
            "Avon",
            "New Patienceburgh",
            "28441",
            "Turkey",
            "1803 637401",
            date,
            time,
            1,
        ]
    ]
    expected_df = pd.DataFrame(
        data,
        columns=[
            "address_id",
            "address_line_1",
            "address_line_2",
            "district",
            "city",
            "postal_code",
            "country",
            "phone",
            "last_updated_date",
            "last_updated_time",
            "location_record_id",
        ],
    )
    pd.set_option("display.max_columns", 11)
    transformed_df = transform_address_table(df)
    expected_df = expected_df.astype(
        {col: "int32" for col in expected_df.select_dtypes("int64").columns}
    )

    assert transformed_df.equals(expected_df)
