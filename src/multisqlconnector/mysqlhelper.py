import random
from datetime import datetime

import mysql.connector

from . import db_config


def get_mysql_connection_parameters(connection=None):
    try:
        if connection is not None and isinstance(connection, dict):
            return connection
        elif db_config.mysql_config is not None and isinstance(db_config.mysql_config, dict):
            return db_config.mysql_config
        else:
            raise ValueError("MySQL connection parameters are not properly configured.")
    except Exception as e:
        raise Exception(f"Error getting MySQL connection parameters: {e}")

#: TODO: Add a function to initialize the MySQL database and create the test table if it doesn't exist. Using sql script to create the db and tables.
def init_mysql_db(connection=None):
    try:
        # Create a database if it doesn't exist
        mysql_config = get_mysql_connection_parameters(connection).copy()
        database_name = mysql_config.get("database")

        database_created = mysql_execute(
            f"""
            CREATE DATABASE IF NOT EXISTS `{database_name}`
            CHARACTER SET utf8mb4
            COLLATE utf8mb4_unicode_ci
            """,
            connection=mysql_config,
        )
        if not database_created:
            return False

        test_table_created = mysql_execute(
            """
            CREATE TABLE IF NOT EXISTS testtable (
                id INT AUTO_INCREMENT PRIMARY KEY,
                value1 INT NULL,
                value2 VARCHAR(255) NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            connection=connection or mysql_config,
        )
        return test_table_created
    except Exception as e:
        raise Exception(f"Error initializing MySQL database: {e}")


def mysql_execute(sqlquery, parameters=None, connection=None):
    conn = None
    cur = None
    try:
        conn_config = get_mysql_connection_parameters(connection) if connection is None else connection
        # CREATE DATABASE must connect at server level (without selecting a DB first).
        if isinstance(sqlquery, str) and "CREATE DATABASE" in sqlquery.upper():
            conn_config = conn_config.copy()
            conn_config.pop("database", None)
        conn = mysql.connector.connect(**conn_config)
        cur = conn.cursor()
        if parameters is not None:
            cur.execute(sqlquery, parameters)
        else:
            cur.execute(sqlquery)
        conn.commit()
        return True
    except Exception as e:
        raise Exception(f"Error at mysql_execute: {e}")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def mysql_select(sqlquery, parameters=None, connection=None):
    conn = None
    cur = None
    try:
        conn_config = get_mysql_connection_parameters(connection) if connection is None else connection
        conn = mysql.connector.connect(**conn_config)
        cur = conn.cursor()
        if parameters is not None:
            cur.execute(sqlquery, parameters)
        else:
            cur.execute(sqlquery)
        return cur.fetchall()
    except Exception as e:
        raise Exception(f"Error at mysql_select: {e}")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def mysql_insert(sqlquery, parameters=None, many=False, connection=None):
    conn = None
    cur = None
    try:
        conn_config = get_mysql_connection_parameters(connection) if connection is None else connection
        conn = mysql.connector.connect(**conn_config)
        cur = conn.cursor()
        if many:
            cur.executemany(sqlquery, parameters or [])
            conn.commit()
            return cur.rowcount
        if parameters is not None:
            cur.execute(sqlquery, parameters)
        else:
            cur.execute(sqlquery)
        conn.commit()
        return cur.lastrowid
    except Exception as e:
        raise Exception(f"Error at mysql_insert: {e}")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def mysql_update(sqlquery, parameters=None, connection=None):
    conn = None
    cur = None
    try:
        conn_config = get_mysql_connection_parameters(connection) if connection is None else connection
        conn = mysql.connector.connect(**conn_config)
        cur = conn.cursor()
        if parameters is not None:
            cur.execute(sqlquery, parameters)
        else:
            cur.execute(sqlquery)
        conn.commit()
        return cur.rowcount
    except Exception as e:
        raise Exception(f"Error at mysql_update: {e}")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def mysql_delete(sqlquery, parameters=None, connection=None):
    conn = None
    cur = None
    try:
        conn_config = get_mysql_connection_parameters(connection) if connection is None else connection
        conn = mysql.connector.connect(**conn_config)
        cur = conn.cursor()
        if parameters is not None:
            cur.execute(sqlquery, parameters)
        else:
            cur.execute(sqlquery)
        conn.commit()
        return cur.rowcount
    except Exception as e:
        raise Exception(f"Error at mysql_delete: {e}")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def mysql_test_functions(connection=None):
    try:
        mysql_config = get_mysql_connection_parameters(connection).copy()
        database_name = mysql_config.get("database")
        print("======== Running MySQL Test Functions =======================")
        print(f"======  Using connection: {database_name} ======")
        mysql_config = get_mysql_connection_parameters(connection).copy()
        print(f"Using database: {database_name}")
        mysql_config = get_mysql_connection_parameters(connection).copy()
        mysql_insert(
            "INSERT INTO testtable (value1, value2) VALUES (%s, %s)",
            (random.randint(1, 100), f"{database_name}_" + str(datetime.now().isoformat()))
        )

        results = mysql_select("SELECT * FROM testtable LIMIT 5")
        for row in results:
            print(row)

        results = mysql_select(
            "SELECT * FROM testtable WHERE id <= %s ORDER BY id DESC LIMIT %s",
            (10, 5)
        )
        for row in results:
            print(row)

        mysql_update(
            "UPDATE testtable SET value2 = %s WHERE id = %s",
            (f"updated_{database_name}_" + str(random.randint(1, 100)), 1)
        )

        topid = mysql_select("SELECT MAX(id) FROM testtable")
        top_id = None
        if isinstance(topid, (list, tuple)) and len(topid) > 0:
            row = topid[0]
            if isinstance(row, (list, tuple)) and len(row) > 0:
                top_id = row[0]

        print(f"Top ID results: {topid if topid else 'N/A'}")
        print(f"Top ID: {top_id if top_id is not None else 'N/A'}")

        first_id = 1
        mysql_delete(
            "DELETE FROM testtable WHERE id = %s",
            (first_id,) if first_id is not None else (0,)
        )
    except Exception as e:
        raise Exception(f"Error at mysql_test_functions: {e}")
