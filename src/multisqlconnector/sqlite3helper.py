import random
import sqlite3
from datetime import datetime
from typing import Any, Sequence

from . import db_config

def get_sqlite_database_path(sqlite_db_path: str | None = None):
    try:
        errormsg = "sqlite_db_path cannot be an empty string or None. Set a valid path using the configure function!"
        if sqlite_db_path is not None and sqlite_db_path.strip() == "":
            raise ValueError(errormsg)
        if db_config.SQLITE_DB_PATH is None or (db_config.SQLITE_DB_PATH is not None and db_config.SQLITE_DB_PATH.strip() == ""):
            raise ValueError(errormsg)
        path = sqlite_db_path if sqlite_db_path is not None else db_config.SQLITE_DB_PATH
        return path
    except Exception as e:
        raise Exception(f"Error getting SQLite database path in get_sqlite_database_path: sqlite_db_path={sqlite_db_path}, {e}")


def get_sqlite_connection(sqlite_db_path: str | None = None):
    try:
        db_path = get_sqlite_database_path(sqlite_db_path)
        return sqlite3.connect(db_path)
    except Exception as e:
        raise Exception(f"Error getting SQLite connection in get_sqlite_connection: sqlite_db_path={sqlite_db_path}, {e}")


def init_sqlite_db(conn: str | None = None, createscript: str | None = None):
    try:
        # it prevents the case where conn is None and python caches a default old value instead of using the provided parameter (Yeah I know. WTF!?)
        resolved_conn = conn if conn is not None else db_config.SQLITE_DB_PATH

        if createscript is None or createscript.strip() == "":
            raise ValueError("createscript cannot be empty")

        sqlite_db_created = sqlite_execute(sqlquery=createscript, parameters=None, connection=resolved_conn)
        return sqlite_db_created
    except Exception as e:
        raise Exception(f"Error initializing SQLite database: {e}")


def sqlite_execute(sqlquery: str, parameters: Sequence[Any] | None = None, connection=None):
    print(f"sqlite_execute conn: {connection}")
    conn = None
    cur = None
    try:
        conn = get_sqlite_connection(connection)
        cur = conn.cursor()
        if parameters is None and isinstance(sqlquery, str) and ";" in sqlquery:
            cur.executescript(sqlquery)
        elif parameters is not None:
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
        conn = get_sqlite_connection(connection)
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
        conn = get_sqlite_connection(connection)
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
        conn = get_sqlite_connection(connection)
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
        conn = get_sqlite_connection(connection)
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
    try:
        db_path = get_sqlite_database_path(connection)
        print("======== Running SQLite Test Functions ======================")
        print(f"======  Using connection: {db_path} ======")
        sqlite_insert(
            "INSERT INTO testtable (value1, value2) VALUES (?, ?)",
            (random.randint(1, 100), f"{db_path} - {str(datetime.now().isoformat())}"),
            connection=connection,
        )

        results = sqlite_select("SELECT * FROM testtable LIMIT 5", connection=connection)
        for row in results:
            print(row)

        results = sqlite_select(
            "SELECT * FROM testtable WHERE id <= ? ORDER BY id DESC LIMIT ?",
            (10, 5),
            connection=connection,
        )
        for row in results:
            print(row)

        sqlite_update(
            "UPDATE testtable SET value2 = ? WHERE id = ?",
            ("updated_value_" + str(random.randint(1, 100)), 1),
            connection=connection,
        )

        topid = sqlite_select(
            "SELECT MAX(id) FROM testtable", connection=connection
        )
        top_id = None
        if isinstance(topid, (list, tuple)) and len(topid) > 0:
            row = topid[0]
            if isinstance(row, (list, tuple)) and len(row) > 0:
                top_id = row[0]

        print(f"Top ID results: {topid if topid else 'N/A'}")
        print(f"Top ID: {top_id if top_id is not None else 'N/A'}")

        first_id = 1
        sqlite_delete(
            "DELETE FROM testtable WHERE id = ?",
            (first_id,) if first_id is not None else (0,),
            connection=connection,
        )
    except Exception as e:
        raise Exception(f"Error at sqlite_test_functions: {e}")
