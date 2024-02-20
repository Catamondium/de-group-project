import pandas as pd
from src.transform_currency_table import transform_currency


def test_map_code_to_name():
    pqt_file = "./test/parquet_test_file"
    df = pd.read_parquet(pqt_file, engine="pyarrow")

    update_df = transform_currency(df)

    ts = pd.Timestamp("2022-11-03T14:20:49.962")
    time = ts.time()
    date = ts.date()

    data = [
        [1, "GBP", "British Pound", date, time],
        [2, "USD", "US Dollar", date, time],
        [3, "EUR", "Euro", date, time],
    ]
    expected_df = pd.DataFrame(
        data,
        columns=[
            "currency_id",
            "currency_code",
            "currency_name",
            "last_updated_date",
            "last_updated_time",
        ]
    )

    assert update_df.equals(expected_df)
