def transform_payment_type_table(df):
    df["last_updated_date"] = df["last_updated"].dt.date
    df["last_updated_time"] = df["last_updated"].dt.time
    df["payment_type_record_id"] = df["payment_type_id"]
    df["payment_record_id"] = df["payment_type_id"]
    df.drop(columns=["last_updated",
                     "created_at",
                     "payment_type_id"],
            inplace=True)
    return df
