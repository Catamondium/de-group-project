def transform_transaction_table(df):
    df["last_updated_date"] = df["last_updated"].dt.date
    df["last_updated_time"] = df["last_updated"].dt.time
    df["transaction_record_id"] = df["transaction_id"]

    df.drop(columns=["last_updated",
                     "created_at",
                     ],
            inplace=True)

    return df
