import pandas as pd
from src.transformation_dictionary import (split_time,
                                           payment_transformation,
                                           purchase_order_transformation,
                                           sales_order_transformation)


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
    result_df = split_time(df,
                           'datetime_col',
                           'date', 'time')

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
        'payment_id', 'created_date', 'created_time', 'payment_record_id',
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

    # Check if dataframe
    assert (df['payment_id'] == df['payment_record_id']).all(), \
        "Columns should be identical."


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

    assert 'payment_record_id' in transformed_df.columns, \
        "payment_record_id is existing in the transformed columns."
    assert 'payment_id' in transformed_df.columns, \
        "payment_id is existing in the transformed columns."
    assert 'transaction_record_id' in transformed_df.columns, \
        "transaction_id was not renamed to transaction_record_id."
    assert 'counterparty_record_id' in transformed_df.columns, \
        "counterparty_id was not renamed to counterparty_record_id."
    assert 'currency_record_id' in transformed_df.columns, \
        "currency_id was not renamed to currency_record_id."
    assert 'payment_type_record_id' in transformed_df.columns, \
        "payment_type_id was not renamed to payment_type_record_id."


def test_purchase_order_transformation():
    # Test data setup
    test_data = {
        'purchase_order_id': [1, 2],
        'created_at': ['2024-01-01 12:00:00', '2024-01-02 13:00:00'],
        'last_updated': ['2024-01-03 14:00:00', '2024-01-04 15:00:00'],
        'staff_id': [101, 102],
        'counterparty_id': [201, 202],
        'item_code': ['X123', 'Y456'],
        'item_quantity': [10, 20],
        'item_unit_price': [100.0, 200.0],
        'currency_id': [1, 2],
        'agreed_delivery_date': ['2024-02-01', '2024-02-02'],
        'agreed_payment_date': ['2024-03-01', '2024-03-02'],
        'agreed_delivery_location_id': [301, 302]
    }
    df = pd.DataFrame(test_data)

    # Expected columns after transformation
    expected_columns = [
        'purchase_record_id', 'purchase_order_id', 'created_date',
        'created_time', 'last_updated_date', 'last_updated_time',
        'staff_record_id', 'counterparty_record_id',
        'item_code', 'item_quantity', 'item_unit_price',
        'currency_record_id', 'agreed_delivery_date',
        'agreed_payment_date', 'agreed_delivery_location_id'
    ]

    # Apply transformation
    new_df = purchase_order_transformation(df)

    # Verify transformation results
    assert all(column in new_df.columns
               for column in expected_columns), \
        "Not all expected columns are present after transformation."

    # Check if 'purchase_order_id' was duplicated correctly
    assert (
            new_df['purchase_order_id'] == new_df['purchase_record_id']
    ).all(), \
        "purchase_order_id was not correctly duplicated to purchase_record_id."

    # Check renaming and splitting operations
    assert 'staff_record_id' in new_df.columns, \
        "staff_id was not renamed to staff_record_id."
    assert 'counterparty_record_id' in new_df.columns, \
        "counterparty_id was not renamed to counterparty_record_id."
    assert 'currency_record_id' in new_df.columns, \
        "currency_id was not renamed to currency_record_id."
    assert ('created_date' in new_df.columns
            and 'created_time' in new_df.columns), \
        "created_at was not correctly split."
    assert ('last_updated_date' in new_df.columns
            and 'last_updated_time' in new_df.columns), \
        "last_updated was not correctly split."


def test_sales_order_transformation():
    # Test data setup
    test_data = {
        'sales_order_id': [1, 2],
        'created_at': ['2024-01-01 12:00:00', '2024-01-02 13:00:00'],
        'last_updated': ['2024-01-03 14:00:00', '2024-01-04 15:00:00'],
        'design_id': [101, 102],
        'staff_id': [201, 202],
        'counterparty_id': [301, 302],
        'currency_id': [1, 2],
        'agreed_delivery_date': ['2024-02-01', '2024-02-02'],
        'agreed_payment_date': ['2024-03-01', '2024-03-02'],
        'agreed_delivery_location_id': [401, 402],
        'units_sold': [10, 20],
        'unit_price': [100.0, 200.0]
    }
    df = pd.DataFrame(test_data)

    # Expected columns after transformation
    expected_columns = [
        'sales_record_id', 'sales_order_id', 'created_date', 'created_time',
        'last_updated_date', 'last_updated_time', 'design_record_id',
        'sales_staff_id',
        'counterparty_record_id', 'currency_record_id', 'units_sold',
        'unit_price',
        'agreed_payment_date', 'agreed_delivery_date',
        'agreed_delivery_location_id'
    ]

    # Apply transformation
    transformed_df = sales_order_transformation(df)

    # Verify transformation results
    assert all(column in transformed_df.columns for column in
               expected_columns), \
        "Not all expected columns are present after transformation."

    # Check if 'sales_order_id' was duplicated correctly
    assert (transformed_df['sales_order_id'] == transformed_df[
        'sales_record_id']).all(), \
        "sales_order_id was not correctly duplicated to sales_record_id."

    # Check renaming and splitting operations
    assert 'design_record_id' in transformed_df.columns, \
        "design_id was not renamed to design_record_id."
    assert 'sales_staff_id' in transformed_df.columns, \
        "staff_id was not renamed to sales_staff_id."
    assert 'counterparty_record_id' in transformed_df.columns, \
        "counterparty_id was not renamed to counterparty_record_id."
    assert 'currency_record_id' in transformed_df.columns, \
        "currency_id was not renamed to currency_record_id."
    assert ('created_date' in transformed_df.columns
            and 'created_time' in transformed_df.columns), \
        "created_at was not correctly split."
    assert ('last_updated_date' in transformed_df.columns
            and 'last_updated_time' in transformed_df.columns), \
        "last_updated was not correctly split."
