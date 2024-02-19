import awswrangler as wr
import os


def get_df_from_parquet(key):
    bucket = os.environ["S3_EXTRACT_BUCKET"]
    pqt_object = [f"s3://{bucket}/{key}"]
    df = wr.s3.read_parquet(path=pqt_object)
    return df
