# anticipated table structure
TABLES = ["currency",
          "payment",
          "department",
          "transaction",
          "design",
          "address",
          "staff",
          "counterparty",
          "purchase_order",
          "payment_type",
          "sales_order"]


def get_query(table: str, last_successful_update_time: str) -> str:
    """
    Generates a SQL query string for a given table and the last
    successful update time.

    The function returns a SELECT query that fetches records from
    the specified table which have been updated on or after the last
    successful update time. It accounts for various relationships
    between the 'table' and other related tables to fetch the updated
    records. If the table name doesn't match any predefined tables,
    it returns a default query.

    Parameters:
    - table (str): The name of the table for which the
        query is to be generated.
    - last_successful_update_time (str): The timestamp of the last
        successful update in the format 'YYYY-MM-DD HH:MM:SS.ssssss'.

    Returns:
    - str: A SQL query string.
    """
    queries = {
            "design": f'''
            SELECT DISTINCT de.*
            FROM design de
            LEFT JOIN sales_order so
                ON de.design_id = so.design_id
            LEFT JOIN transaction t
                ON so.sales_order_id = t.purchase_order_id
            LEFT JOIN payment pa
                ON t.transaction_id = pa.transaction_id
            WHERE de.last_updated >= '{last_successful_update_time}'
                OR so.last_updated >= '{last_successful_update_time}'
                OR t.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}';''',

            "payment_type": f'''
            SELECT DISTINCT pt.*
            FROM payment_type pt
            LEFT JOIN payment pa
                ON pt.payment_type_id = pa.payment_type_id
            WHERE pt.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}';''',

            "payment": f'''
            SELECT * FROM payment
            WHERE last_updated > '{last_successful_update_time}';''',

            "currency": f'''
            SELECT DISTINCT cu.*
            FROM currency cu
            LEFT JOIN payment pa
                ON cu.currency_id = pa.currency_id
            WHERE cu.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}'

            UNION

            SELECT DISTINCT cu.*
            FROM currency cu
            LEFT JOIN purchase_order po
                ON cu.currency_id = po.currency_id
            LEFT JOIN transaction t
                ON po.purchase_order_id = t.purchase_order_id
            LEFT JOIN payment pa
                ON t.transaction_id = pa.transaction_id
            WHERE cu.last_updated >= '{last_successful_update_time}'
                OR po.last_updated >= '{last_successful_update_time}'
                OR t.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}'

            UNION

            SELECT DISTINCT cu.*
            FROM currency cu
            LEFT JOIN sales_order so
                ON cu.currency_id = so.currency_id
            LEFT JOIN transaction t
                ON so.sales_order_id = t.purchase_order_id
            LEFT JOIN payment pa
                ON t.transaction_id = pa.transaction_id
            WHERE cu.last_updated >= '{last_successful_update_time}'
                OR so.last_updated >= '{last_successful_update_time}'
                OR t.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}';''',

            "department": f'''
            SELECT DISTINCT d.*
            FROM department d
            LEFT JOIN staff st
                ON d.department_id = st.department_id
            LEFT JOIN purchase_order po
                ON st.staff_id = po.staff_id
            LEFT JOIN transaction t
                ON po.purchase_order_id = t.purchase_order_id
            LEFT JOIN payment pa
                ON t.transaction_id = pa.transaction_id
            WHERE d.last_updated >= '{last_successful_update_time}'
                OR st.last_updated >= '{last_successful_update_time}'
                OR po.last_updated >= '{last_successful_update_time}'
                OR t.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}'

            UNION

            SELECT DISTINCT d.*
            FROM department d
            LEFT JOIN staff st
                ON d.department_id = st.department_id
            LEFT JOIN sales_order so
                ON st.staff_id = so.staff_id
            LEFT JOIN transaction t
                ON so.sales_order_id = t.purchase_order_id
            LEFT JOIN payment pa
                ON t.transaction_id = pa.transaction_id
            WHERE d.last_updated >= '{last_successful_update_time}'
                OR st.last_updated >= '{last_successful_update_time}'
                OR so.last_updated >= '{last_successful_update_time}'
                OR t.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}';''',

            "transaction": f'''
            SELECT DISTINCT tr.*
            FROM transaction tr
            LEFT JOIN payment pa
                ON tr.transaction_id = pa.transaction_id
            WHERE tr.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}';''',

            "address": f'''
            SELECT DISTINCT a.*
            FROM address a
            LEFT JOIN counterparty c
               ON a.address_id = c.legal_address_id
            LEFT JOIN purchase_order po
              ON c.counterparty_id = po.counterparty_id
            LEFT JOIN transaction t
                ON po.purchase_order_id = t.purchase_order_id
            LEFT JOIN payment pa
                ON t.transaction_id = pa.transaction_id
            WHERE a.last_updated >= '{last_successful_update_time}'
                OR c.last_updated >= '{last_successful_update_time}'
                OR po.last_updated >= '{last_successful_update_time}'
                OR t.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}'

            UNION

            SELECT DISTINCT a.*
            FROM address a
            LEFT JOIN counterparty c
                ON a.address_id = c.legal_address_id
            LEFT JOIN payment p
                ON c.counterparty_id = p.counterparty_id
            WHERE a.last_updated >= '{last_successful_update_time}'
                OR c.last_updated >= '{last_successful_update_time}'
                OR p.last_updated >= '{last_successful_update_time}'

            UNION

            SELECT DISTINCT a.*
            FROM address a
            LEFT JOIN counterparty c
                ON a.address_id = c.legal_address_id
            LEFT JOIN sales_order so
                ON c.counterparty_id = so.counterparty_id
            LEFT JOIN transaction t
                ON so.sales_order_id = t.sales_order_id
            LEFT JOIN payment pa
                ON t.transaction_id = pa.transaction_id
            WHERE a.last_updated >= '{last_successful_update_time}'
                OR c.last_updated >= '{last_successful_update_time}'
                OR so.last_updated >= '{last_successful_update_time}'
                OR t.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}'

            UNION

            SELECT DISTINCT a.*
            FROM address a
            LEFT JOIN purchase_order po
                  ON a.address_id = po.agreed_delivery_location_id
            LEFT JOIN transaction t
                ON po.purchase_order_id = t.purchase_order_id
            LEFT JOIN payment pa
                ON t.transaction_id = pa.transaction_id
            WHERE a.last_updated >= '{last_successful_update_time}'
                OR po.last_updated >= '{last_successful_update_time}'
                OR t.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}'

            UNION

            SELECT DISTINCT a.*
            FROM address a
            LEFT JOIN sales_order so
                ON a.address_id = so.agreed_delivery_location_id
            LEFT JOIN transaction t
                ON so.sales_order_id = t.sales_order_id
            LEFT JOIN payment pa
                ON t.transaction_id = pa.transaction_id
            WHERE a.last_updated >= '{last_successful_update_time}'
                OR so.last_updated >= '{last_successful_update_time}'
                OR t.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}';''',

            "staff": f'''
            SELECT DISTINCT st.*
            FROM staff st
            LEFT JOIN purchase_order po
                ON st.staff_id = po.staff_id
            LEFT JOIN transaction t
                ON po.purchase_order_id = t.purchase_order_id
            LEFT JOIN payment pa
                ON t.transaction_id = pa.transaction_id
            WHERE st.last_updated >= '{last_successful_update_time}'
                OR po.last_updated >= '{last_successful_update_time}'
                OR t.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}'

            UNION

            SELECT DISTINCT st.*
            FROM staff st
            LEFT JOIN sales_order so
                ON st.staff_id = so.staff_id
            LEFT JOIN transaction t
                ON so.sales_order_id = t.purchase_order_id
            LEFT JOIN payment pa
                ON t.transaction_id = pa.transaction_id
            WHERE st.last_updated >= '{last_successful_update_time}'
                OR so.last_updated >= '{last_successful_update_time}'
                OR t.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}';''',

            "counterparty": f'''
            SELECT DISTINCT co.*
            FROM counterparty co
            LEFT JOIN payment pa
                ON co.counterparty_id = pa.counterparty_id
            WHERE co.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}'

            UNION

            SELECT DISTINCT co.*
            FROM counterparty co
            LEFT JOIN purchase_order po
                ON co.counterparty_id = po.counterparty_id
            LEFT JOIN transaction t
                ON po.purchase_order_id = t.purchase_order_id
            LEFT JOIN payment pa
                ON t.transaction_id = pa.transaction_id
            WHERE co.last_updated >= '{last_successful_update_time}'
                OR po.last_updated >= '{last_successful_update_time}'
                OR t.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}'

            UNION

            SELECT DISTINCT co.*
            FROM counterparty co
            LEFT JOIN sales_order so
                ON co.counterparty_id = so.counterparty_id
            LEFT JOIN transaction t
                ON so.sales_order_id = t.purchase_order_id
            LEFT JOIN payment pa
                ON t.transaction_id = pa.transaction_id
            WHERE co.last_updated >= '{last_successful_update_time}'
                OR so.last_updated >= '{last_successful_update_time}'
                OR t.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}';''',

            "purchase_order": f'''
            SELECT DISTINCT po.*
            FROM purchase_order po
            LEFT JOIN transaction t
                ON po.purchase_order_id = t.purchase_order_id
            LEFT JOIN payment pa
                ON t.transaction_id = pa.transaction_id
            WHERE po.last_updated >= '{last_successful_update_time}'
                OR t.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}';''',

            "sales_order": f'''
            SELECT DISTINCT so.*
            FROM sales_order so
            LEFT JOIN transaction t
                ON so.sales_order_id = t.sales_order_id
            LEFT JOIN payment pa
                ON t.transaction_id = pa.transaction_id
            WHERE so.last_updated >= '{last_successful_update_time}'
                OR t.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}';''',

            # default
            "default": f'''
                SELECT * FROM {table}
                WHERE last_updated >= '{last_successful_update_time}';'''
    }
    if table in TABLES:
        return queries[table]
    else:
        return queries["default"]
