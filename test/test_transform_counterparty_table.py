import pandas as pd
from transform_counterparty_table import transform_counterparty_table


def test_transform_counterpary_table():
    pqt_file = "./test/parquet_test_file/counterparty.pqt"

    df = pd.read_parquet(pqt_file, engine="pyarrow")

    ts = pd.Timestamp("2022-11-03T14:20:51.563")
    date = ts.date()
    time = ts.time()

    data = [
        [
            1,
            "Fahey and Sons",
            "605 Haskell Trafficway",
            "Axel Freeway",
            None,
            "East Bobbie",
            "88253-4257",
            "Heard Island and McDonald Islands",
            "9687 937447",
            date,
            time,
            1,
        ]
    ]
    expected_df = pd.DataFrame(
        data,
        columns=[
            "counterparty_id",
            "counterparty_legal_name",
            "counterparty_legal_address_line_1",
            "counterparty_legal_address_line_2",
            "counterparty_legal_district",
            "counterparty_legal_city",
            "counterparty_legal_postal_code",
            "counterparty_legal_country",
            "counterparty_legal_phone_number",
            "last_updated_date",
            "last_updated_time",
            "counterparty_record_id",
        ],
    )
    transformed_df = transform_counterparty_table(df)
    expected_df = expected_df.astype(
        {col: "int32" for col in expected_df.select_dtypes("int64").columns}
    )

    for column, _ in transformed_df.items():
        assert transformed_df[column][0] == expected_df[column][0]
