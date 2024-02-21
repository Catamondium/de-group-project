def transform_counterparty_table(df):

    df["last_updated_date"] = df["last_updated"].dt.date
    df["last_updated_time"] = df["last_updated"].dt.time

    df["counterparty_record_id"] = df["counterparty_id"]

    rename_dict = {
        "address_line_1": "counterparty_legal_address_line_1",
        "address_line_2": "counterparty_legal_address_line_2",
        "district": "counterparty_legal_district",
        "city": "counterparty_legal_city",
        "postal_code": "counterparty_legal_postal_code",
        "country": "counterparty_legal_country",
        "phone": "counterparty_legal_phone_number",
    }
    df.rename(columns=rename_dict, inplace=True)

    df.drop(
        columns=[
            "last_updated",
            "created_at",
            "legal_address_id",
            "commercial_contact",
            "delivery_contact",
        ],
        inplace=True,
    )
    return df
