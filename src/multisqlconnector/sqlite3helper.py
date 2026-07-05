import random
import sqlite3
from datetime import datetime
from typing import Any, Sequence

from . import db_config


def get_default_sqlite_connection():
    return sqlite3.connect(db_config.SQLITE_DB_PATH)


def sqlite_execute(sqlquery: str, parameters: Sequence[Any] | None = None, connection=None):
    conn = None
    cur = None
    try:
        conn = connection or get_default_sqlite_connection()
        cur = conn.cursor()
        if parameters is not None:
            cur.execute(sqlquery, parameters)
        else:
            cur.execute(sqlquery)
        conn.commit()
        return True
    except Exception as e:
        raise Exception(f"Error at sqlite_execute: {e}")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def sqlite_select(sqlquery: str, parameters: Sequence[Any] | None = None, connection=None):
    conn = None
    cur = None
    try:
        conn = connection or get_default_sqlite_connection()
        cur = conn.cursor()
        if parameters is not None:
            cur.execute(sqlquery, parameters)
        else:
            cur.execute(sqlquery)
        return cur.fetchall()
    except Exception as e:
        raise Exception(f"Error at sqlite_select: {e}")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def sqlite_insert(
    sqlquery: str,
    parameters: Sequence[Any] | Sequence[Sequence[Any]] | None = None,
    many: bool = False,
    connection=None,
):
    conn = None
    cur = None
    try:
        conn = connection or get_default_sqlite_connection()
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
        raise Exception(f"Error at sqlite_insert: {e}")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def sqlite_update(sqlquery: str, parameters: Sequence[Any] | None = None, connection=None):
    conn = None
    cur = None
    try:
        conn = connection or get_default_sqlite_connection()
        cur = conn.cursor()
        if parameters is not None:
            cur.execute(sqlquery, parameters)
        else:
            cur.execute(sqlquery)
        conn.commit()
        return cur.rowcount
    except Exception as e:
        raise Exception(f"Error at sqlite_update: {e}")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def sqlite_delete(sqlquery: str, parameters: Sequence[Any] | None = None, connection=None):
    conn = None
    cur = None
    try:
        conn = connection or get_default_sqlite_connection()
        cur = conn.cursor()
        if parameters is not None:
            cur.execute(sqlquery, parameters)
        else:
            cur.execute(sqlquery)
        conn.commit()
        return cur.rowcount
    except Exception as e:
        raise Exception(f"Error at sqlite_delete: {e}")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def sqlite_test_functions(connection=None):
    def effective_connection():
        return connection if connection is not None else get_default_sqlite_connection()

    try:
        sqlite_insert(
            "INSERT INTO testtable (value1, value2) VALUES (?, ?)",
            (random.randint(1, 100), "datetime_" + str(datetime.now().isoformat())),
            connection=effective_connection(),
        )

        results = sqlite_select("SELECT * FROM testtable LIMIT 5", connection=effective_connection())
        for row in results:
            print(row)

        results = sqlite_select(
            "SELECT * FROM testtable WHERE id <= ? ORDER BY id DESC LIMIT ?",
            (10, 5),
            connection=effective_connection(),
        )
        for row in results:
            print(row)

        sqlite_update(
            "UPDATE testtable SET value2 = ? WHERE id = ?",
            ("updated_value_" + str(random.randint(1, 100)), 1),
            connection=effective_connection(),
        )

        topid = sqlite_select(
            "SELECT MAX(id) FROM testtable", connection=effective_connection()
        )
        top_id = None
        if isinstance(topid, (list, tuple)) and len(topid) > 0:
            row = topid[0]
            if isinstance(row, (list, tuple)) and len(row) > 0:
                top_id = row[0]

        print(f"Top ID results: {topid if topid else 'N/A'}")
        print(f"Top ID: {top_id if top_id is not None else 'N/A'}")

        delete_id = 1
        sqlite_delete(
            "DELETE FROM testtable WHERE id = ?",
            (delete_id,) if delete_id is not None else (0,),
            connection=effective_connection(),
        )
    except Exception as e:
        raise Exception(f"Error at sqlite_test_functions: {e}")
