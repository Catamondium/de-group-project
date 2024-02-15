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


def get_query(table, last_successful_update_time):
    queries = {
            # todo: fix
            "design": f'''
            SELECT DISTINCT de.*
            FROM design de
            INNER JOIN sales_order so
                ON de.design_id = so.design_id
            INNER JOIN transaction t
                ON so.sales_order_id = t.purchase_order_id
            INNER JOIN payment pa
                ON t.transaction_id = pa.transaction_id
            WHERE de.last_updated >= '{last_successful_update_time}'
                OR so.last_updated >= '{last_successful_update_time}'
                OR t.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}';''',

            "payment_type": f'''
            SELECT * FROM payment_type
            WHERE last_updated > '{last_successful_update_time}'
            UNION
            SELECT pt.* FROM payment_type pt
            INNER JOIN payment p ON pt.payment_type_id = p.payment_type_id
            WHERE p.last_updated > '{last_successful_update_time}';''',

            "payment": f'''
            SELECT * FROM payment
            WHERE last_updated > '{last_successful_update_time}';''',

            "currency": f'''
            SELECT * FROM currency
            WHERE last_updated >= '{last_successful_update_time}'
            UNION
            SELECT * FROM currency WHERE currency_id in
            (SELECT currency_id
            FROM payment
            WHERE last_updated >= '{last_successful_update_time}')
            UNION
            (SELECT DISTINCT c.* FROM currency c
            INNER JOIN purchase_order po ON c.currency_id = po.currency_id
            INNER JOIN transaction t
            ON po.purchase_order_id = t.purchase_order_id
            WHERE T.created_at > '{last_successful_update_time}')
            UNION
            (SELECT DISTINCT c.* FROM currency c
            INNER JOIN sales_order co ON c.currency_id = co.currency_id
            INNER JOIN transaction t ON co.sales_order_id = t.sales_order_id
            WHERE T.created_at > '{last_successful_update_time}');''',

            # todo deps
            "department": f'''
            SELECT * FROM department
            WHERE last_updated >= '{last_successful_update_time}';''',

            "transaction": f'''
            SELECT * FROM transaction
            WHERE last_updated >= '{last_successful_update_time}';
            UNION
            SELECT t.* FROM transaction t
            INNER JOIN payment p ON t.transaction_id = p.transaction_id
            WHERE p.last_updated >= '{last_successful_update_time}';''',

            "address": f'''SELECT DISTINCT a.*
            FROM address a
            LEFT JOIN counterparty c
            ON a.address_id = c.legal_address_id
            LEFT JOIN purchase_order po
            ON c.counterparty_id = po.counterparty_id
            LEFT JOIN transaction t
            ON po.purchase_order_id = t.purchase_order_id
            LEFT JOIN payment pa ON t.transaction_id = pa.transaction_id
            WHERE a.last_updated >= '{last_successful_update_time}'
                OR c.last_updated >= '{last_successful_update_time}'
                OR po.last_updated >= '{last_successful_update_time}'
                OR t.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}'

            UNION

            SELECT DISTINCT a.*
            FROM address a
            LEFT JOIN counterparty c ON a.address_id = c.legal_address_id
            LEFT JOIN payment p ON c.counterparty_id = p.counterparty_id
            WHERE a.last_updated >= '{last_successful_update_time}'
                OR c.last_updated >= '{last_successful_update_time}'
                OR p.last_updated >= '{last_successful_update_time}'

            UNION

            SELECT DISTINCT a.*
            FROM address a
            LEFT JOIN counterparty c ON a.address_id = c.legal_address_id
            LEFT JOIN sales_order so ON c.counterparty_id = so.counterparty_id
            LEFT JOIN transaction t ON so.sales_order_id = t.sales_order_id
            LEFT JOIN payment pa ON t.transaction_id = pa.transaction_id
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
            LEFT JOIN payment pa ON t.transaction_id = pa.transaction_id
            WHERE a.last_updated >= '{last_successful_update_time}'
                OR po.last_updated >= '{last_successful_update_time}'
                OR t.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}'
            UNION
            SELECT DISTINCT a.*
            FROM address a
            LEFT JOIN sales_order so
                ON a.address_id = so.agreed_delivery_location_id
            LEFT JOIN transaction t ON so.sales_order_id = t.sales_order_id
            LEFT JOIN payment pa ON t.transaction_id = pa.transaction_id
            WHERE a.last_updated >= '{last_successful_update_time}'
                OR so.last_updated >= '{last_successful_update_time}'
                OR t.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}';''',

            # todo staff
            "staff": f'''
            SELECT * FROM staff
            WHERE last_updated >= '{last_successful_update_time}';''',

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
            INNER JOIN purchase_order po
                ON co.counterparty_id = po.counterparty_id
            INNER JOIN transaction t
                ON po.purchase_order_id = t.purchase_order_id
            INNER JOIN payment pa
                ON t.transaction_id = pa.transaction_id
            WHERE co.last_updated >= '{last_successful_update_time}'
                OR po.last_updated >= '{last_successful_update_time}'
                OR t.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}'
            UNION
            SELECT DISTINCT co.*
            FROM counterparty co
            INNER JOIN sales_order so
                ON co.counterparty_id = so.counterparty_id
            INNER JOIN transaction t
                ON so.sales_order_id = t.purchase_order_id
            INNER JOIN payment pa
                ON t.transaction_id = pa.transaction_id
            WHERE co.last_updated >= '{last_successful_update_time}'
                OR so.last_updated >= '{last_successful_update_time}'
                OR t.last_updated >= '{last_successful_update_time}'
                OR pa.last_updated >= '{last_successful_update_time}';''',

            # todo purchase_order
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
