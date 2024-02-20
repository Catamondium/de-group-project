
def transform_design_table(df):
    df["last_updated_date"] = df["last_updated"].dt.date
    df["last_updated_time"] = df["last_updated"].dt.time
    df["design_record_id"] = df["design_id"]
    df.drop(columns=["last_updated", "created_at"], inplace=True)

    return df
