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
    # DUPLICATE payment_id
    df['payment_record_id'] = df['payment_id']
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
    return df


def purchase_order_transformation(df):
    # purchase_order_id RENAME  purchase_record_id
    # AND DUPLICATE to          purchase_order_id

    # created_at SPLIT TO created_date, created_time

    # last_updated SPLIT TO last_updated_date, last_updated_time
    # staff_id
    # counterparty_id
    # item_code
    # item_quantity
    # item_unit_price
    # currency_id
    # agreed_delivery_date
    # agreed_payment_date
    # agreed_delivery_location_id

    # purchase_record_id
    # purchase_order_id

    # created_date
    # created_time

    # last_updated_date
    # last_updated_time
    # staff_record_id
    # counterparty_record_id
    # item_code
    # item_quantity
    # item_unit_price
    # currency_record_id
    # agreed_delivery_date
    # agreed_payment_date
    # agreed_delivery_location_id

    return 0


tables_transformation_templates = {
    "payment_transformation": payment_transformation,
}
