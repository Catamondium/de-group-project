import pandas as pd


def split_time(df,
               col_name,
               new_date_col_name,
               new_time_col_name):
    df[col_name] = pd.to_datetime(df[col_name])

    # split
    df[new_date_col_name] = df[col_name].dt.date
    df[new_time_col_name] = df[col_name].dt.time

    return df


def payment_transformation(df):
    # OLD

    # payment_id - OK
    # created_at - SPLIT
    df = split_time(df, 'created_at',
                    'created_date',
                    'created_time')
    # last_updated - SPLIT
    df = split_time(df, 'last_updated',
                    'last_updated_date',
                    'last_updated_time')
    # transaction_id - RENAME TO transaction_record_id
    df.rename(columns={'transaction_id': 'transaction_record_id'},
              inplace=True)
    # counterparty_id - RENAME TO counterparty_record_id
    df.rename(columns={'counterparty_id': 'counterparty_record_id'},
              inplace=True)
    # payment_amount - OK
    # currency_id - RENAME TO currency_record_id
    df.rename(columns={'currency_id': 'currency_record_id'},
              inplace=True)
    # payment_type_id - RENAME TO payment_type_record_id
    df.rename(columns={'payment_type_id': 'payment_type_record_id'},
              inplace=True)
    # paid - OK
    # payment_date - OK
    # company_ac_number - DELETE
    df.drop('company_ac_number', axis=1, inplace=True)
    # counterparty_ac_number - DELETE
    df.drop('counterparty_ac_number', axis=1, inplace=True)

    # NEW
    # payment_record_id -- new
    # , payment_id, created_date,
    # created_time, lst_updated_date, last_updated_time
    # transaction_record_id, counterparty_record_id
    # payment_amount, currency_record_id
    # payment_type_record_id, paid, payment_date

    return df


tables_transformation_templates = {
    "payment_transformation": payment_transformation,
}
