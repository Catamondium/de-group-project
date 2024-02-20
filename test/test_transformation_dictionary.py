import pandas as pd
from transformation_dictionary import split_time, payment_transformation


def test_split_time():
    test_data = {
        'datetime_col': ['2024-02-13 10:45:18', '2024-02-14 11:30:45']
    }
    expected_date = [pd.to_datetime(d).date()
                     for d in test_data['datetime_col']]
    expected_time = [pd.to_datetime(d).time()
                     for d in test_data['datetime_col']]

    df = pd.DataFrame(test_data)

    # ACT
    result_df = split_time(df, 'datetime_col', 'date', 'time')

    # ASSERT
    assert all(result_df['date'] == expected_date), \
        "The date column does not match expected values."
    assert all(result_df['time'] == expected_time), \
        "The time column does not match expected values."
    assert 'datetime_col' in result_df.columns, \
        "The original datetime column was removed."


def test_payment_transformation_splits_dates():
    # Test data
    test_data = {
        'payment_id': [1, 2],
        'created_at': ['2024-02-13 10:45:18', '2024-02-14 11:30:45'],
        'last_updated': ['2024-02-15 14:20:30', '2024-02-16 15:35:50'],
        'transaction_id': [101, 102],
        'counterparty_id': [201, 202],
        'payment_amount': [300.00, 450.50],
        'currency_id': [1, 2],
        'payment_type_id': [1, 2],
        'paid': [True, False],
        'payment_date': ['2024-02-17', '2024-02-18'],
        'company_ac_number': ['123456', '654321'],
        'counterparty_ac_number': ['987654', '456789']
    }
    df = pd.DataFrame(test_data)

    # Expected columns
    expected_columns = [
        'payment_id', 'created_date', 'created_time',
        'last_updated_date', 'last_updated_time', 'transaction_record_id',
        'counterparty_record_id', 'payment_amount', 'currency_record_id',
        'payment_type_record_id', 'paid', 'payment_date'
    ]

    # Transformation
    transformed_df = payment_transformation(df)

    # Check if all expected columns are in the transformed dataframe
    assert all(column in transformed_df.columns
               for column in expected_columns), \
        "Not all expected columns are present."

    # Check if original columns that should be deleted are removed
    assert 'company_ac_number' not in transformed_df.columns, \
        "company_ac_number was not removed."
    assert 'counterparty_ac_number' not in transformed_df.columns, \
        "counterparty_ac_number was not removed."


def test_payment_transformation_renames_columns():
    test_data = {
        'payment_id': [1, 2],
        'created_at': ['2024-02-13 10:45:18', '2024-02-14 11:30:45'],
        'last_updated': ['2024-02-15 14:20:30', '2024-02-16 15:35:50'],
        'transaction_id': [101, 102],
        'counterparty_id': [201, 202],
        'payment_amount': [300.00, 450.50],
        'currency_id': [1, 2],
        'payment_type_id': [1, 2],
        'paid': [True, False],
        'payment_date': ['2024-02-17', '2024-02-18'],
        'company_ac_number': ['123456', '654321'],
        'counterparty_ac_number': ['987654', '456789'],
    }
    df = pd.DataFrame(test_data)

    transformed_df = payment_transformation(df)

    assert 'transaction_record_id' in transformed_df.columns, \
        "transaction_id was not renamed to transaction_record_id."
    assert 'counterparty_record_id' in transformed_df.columns, \
        "counterparty_id was not renamed to counterparty_record_id."
    assert 'currency_record_id' in transformed_df.columns, \
        "currency_id was not renamed to currency_record_id."
    assert 'payment_type_record_id' in transformed_df.columns, \
        "payment_type_id was not renamed to payment_type_record_id."
