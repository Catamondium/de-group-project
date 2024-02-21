def transform_staff_table(df):
    df["last_updated_date"] = df["last_updated"].dt.date
    df["last_updated_time"] = df["last_updated"].dt.time

    df["staff_record_id"] = df["staff_id"]

    df.drop(columns=["last_updated",
                     "created_at",
                     "department_id"],
            inplace=True)
    return df
