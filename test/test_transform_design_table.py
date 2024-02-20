import pandas as pd
from transform_design_table import transform_design_table


def test_transform_design_table():
    pqt_file = './test/parquet_test_file/design.pqt'
    df = pd.read_parquet(pqt_file, engine="pyarrow")

    transformed_df = transform_design_table(df)

    ts = pd.Timestamp("2024-02-20T13:15:10.121")
    date = ts.date()
    time = ts.time()

    data = [
        [
           320,
           "Granite",
           "/usr/local/src",
           "granite-20230421-evia.json",
           date,
           time,
           320,
        ]
    ]
    expected_df = pd.DataFrame(
        data,
        columns=[
            "design_id",
            "design_name",
            "file_location",
            "file_name",
            "last_updated_date",
            "last_updated_time",
            "design_record_id",
        ]
    )
    expected_df = expected_df.astype(
        {col: 'int32' for col in expected_df.select_dtypes('int64').columns})

    print(expected_df.dtypes, "expected df types")
    assert transformed_df.equals(expected_df)
