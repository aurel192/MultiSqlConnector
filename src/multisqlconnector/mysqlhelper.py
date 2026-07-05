import random
from datetime import datetime

import mysql.connector

from . import db_config


def get_default_mysql_connection():
    return db_config.mysql_config


def mysql_execute(sqlquery, parameters=None, connection=None):
    conn = None
    cur = None
    try:
        conn_config = get_default_mysql_connection() if connection is None else connection
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
        conn_config = get_default_mysql_connection() if connection is None else connection
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
        conn_config = get_default_mysql_connection() if connection is None else connection
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
        conn_config = get_default_mysql_connection() if connection is None else connection
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
        conn_config = get_default_mysql_connection() if connection is None else connection
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
    effective_connection = (
        get_default_mysql_connection() if connection is None else connection
    )

    try:
        mysql_insert(
            "INSERT INTO testtable (value1, value2) VALUES (%s, %s)",
            (random.randint(1, 100), "datetime_" + str(datetime.now().isoformat())),
            connection=effective_connection,
        )

        results = mysql_select("SELECT * FROM testtable LIMIT 5", connection=effective_connection)
        for row in results:
            print(row)

        results = mysql_select(
            "SELECT * FROM testtable WHERE id <= %s ORDER BY id DESC LIMIT %s",
            (10, 5),
            connection=effective_connection,
        )
        for row in results:
            print(row)

        mysql_update(
            "UPDATE testtable SET value2 = %s WHERE id = %s",
            ("updated_value_" + str(random.randint(1, 100)), 1),
            connection=effective_connection,
        )

        topid = mysql_select("SELECT MAX(id) FROM testtable", connection=effective_connection)
        top_id = None
        if isinstance(topid, (list, tuple)) and len(topid) > 0:
            row = topid[0]
            if isinstance(row, (list, tuple)) and len(row) > 0:
                top_id = row[0]

        print(f"Top ID results: {topid if topid else 'N/A'}")
        print(f"Top ID: {top_id if top_id is not None else 'N/A'}")

        delete_id = 1
        mysql_delete(
            "DELETE FROM testtable WHERE id = %s",
            (delete_id,) if delete_id is not None else (0,),
            connection=effective_connection,
        )
    except Exception as e:
        raise Exception(f"Error at mysql_test_functions: {e}")
