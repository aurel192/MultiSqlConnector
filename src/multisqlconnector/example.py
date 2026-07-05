from pathlib import Path
import sys

# Allow direct execution: py src/multisqlconnector/example.py
if __package__ is None or __package__ == "":
    src_root = Path(__file__).resolve().parents[1]
    if str(src_root) not in sys.path:
        sys.path.insert(0, str(src_root))

from multisqlconnector import configure, sql_select, sql_select_cast, sql_select_named
from multisqlconnector import db_config
from multisqlconnector.db_config import mysql_config
from multisqlconnector.mysqlhelper import mysql_execute, mysql_test_functions, init_mysql_db
from multisqlconnector.sqlite3helper import *


def create_db_and_run_tests():
    current_provider = db_config.DEFAULT_SQL_PROVIDER
    print(f"-------- RUNNING TESTS USING: {current_provider} ---------------------")
    if current_provider == "MYSQL":
        created = init_mysql_db()
        if not created:
            print("MySQL database initialization failed.")
            return
        print("MySQL database initialized.")
        mysql_test_functions()
        return

    if current_provider == "SQLITE":
        sqlite_create_script = f"""
            CREATE TABLE IF NOT EXISTS testtable (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value1 INTEGER NULL,
                value2 TEXT NULL
            )
            """
        created = init_sqlite_db(createscript=sqlite_create_script)
        if not created:
            print("SQLite database initialization failed.")
            return
        print("SQLite database created.")
        sqlite_test_functions()
        return

    print(f"Unsupported database type: {current_provider}!")


def run_select_queries():
    current_provider = db_config.DEFAULT_SQL_PROVIDER
    print(f"-------- RUNNING SELECT QUERY ON {current_provider} WITHOUT CASTING ---------------------")
    result = sql_select(
        sqlquery="SELECT id, value1, value2 FROM testtable WHERE id > %p",
        parameters=(2,)
    )

    print(f"Not casted rows: {result}\n")
    for row in result:
        print(f"Row ID: {row[0]}")  # type: ignore[index]
        print(f"Row: {row}")

    print(f"-------- RUNNING SELECT QUERY ON {current_provider} WITH CASTING ---------------------")
    casted_rows = sql_select_cast(
        "SELECT id, value1, value2 FROM testtable WHERE id > %p",
        result_types=(int, int, str),
        parameters=(2,)
    )

    print(f"Casted rows: {casted_rows}\n")
    for row in casted_rows:
        print(f"Row ID: {row[0]}")  # type: ignore[index]
        print(f"Row: {row}")

    print(f"-------- RUNNING SELECT QUERY ON {current_provider} WITH NAMED RESULTS ---------------------")
    named_rows = sql_select_named(
        sqlquery="SELECT id, value1, value2 FROM testtable WHERE id > %p",
        parameters=(2,)
    )

    print(f"Named rows: {named_rows}\n")
    for row in named_rows:
        print(f"Row ID: {row['id']}")
        print(f"Row: {row}")


if __name__ == "__main__":

    sqlite_create_script = f"""
            CREATE TABLE IF NOT EXISTS testtable (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value1 INTEGER NULL,
                value2 TEXT NULL
            )
            """
    other_sqlite3_path = "something_else.db"

    created = init_sqlite_db(createscript=sqlite_create_script)
    print(f"SQLite database created: {created} (or it already existed)")

    # Test SQLITE with custom connection
    created = init_sqlite_db(createscript=sqlite_create_script, connection=other_sqlite3_path)
    print(f"SQLite database created with custom connection: {created} (or it already existed)")

    # Test SQLITE Default connection
    configure(default_sqlprovider="SQLITE", sqlite_db_path="test_sqlite.db")  # Change to "MYSQL" to test MySQL

    sqlite_test_functions()

    create_db_and_run_tests()

    # Test MYSQL Default connection
    configure(default_sqlprovider="MYSQL", mysql_connection=db_config.mysql_config)  # Change to "MYSQL" to test MySQL
    mysql_test_functions()

    custom_mysql_settings: dict[str, Any] = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "1234",
        "database": "test_db_02",
        "charset": "utf8mb4",
        "collation": "utf8mb4_unicode_ci",
    }

    # Test MYSQL with custom reconfigured settings
    configure(default_sqlprovider="MYSQL", mysql_connection=custom_mysql_settings)  # Change to "MYSQL" to test MySQL
    # This will create the database if it doesn't exist. Database name = test_db_02
    init_mysql_db(connection=custom_mysql_settings)
    create_db_and_run_tests()

    print("\n\n==================== Running SELECT queries on both databases ====================")
    configure(default_sqlprovider="SQLITE")
    run_select_queries()

    # configure(default_sqlprovider="MYSQL")
    # run_select_queries()
