from urllib.request import urlopen
from json import loads
import pandas as pd


def transform_currency(df):
    url = "https://raw.githubusercontent.com/umpirsky/currency-list/master/data/en_GB/currency.json"  # noqa
    response = urlopen(url)

    json_raw = response.read().decode("utf-8")
    currencies = loads(json_raw)

    curr_ls = [
        {
            "currency_code": k,
            "currency_name": v,
        }
        for k, v in currencies.items()
    ]

    currency_df = pd.DataFrame(data=curr_ls)

    df = df.merge(currency_df, how="left", on="currency_code", validate="m:1")

    df["last_updated_date"] = df["last_updated"].dt.date
    df["last_updated_time"] = df["last_updated"].dt.time

    df.drop(columns=["last_updated", "created_at"], inplace=True)

    return df
