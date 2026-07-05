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
from multisqlconnector.mysqlhelper import mysql_execute, mysql_test_functions
from multisqlconnector.sqlite3helper import sqlite_execute, sqlite_test_functions


def init_sqlite_db():
    return sqlite_execute(
        """
        CREATE TABLE IF NOT EXISTS testtable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value1 INTEGER NULL,
            value2 TEXT NULL
        )
        """
    )


def init_mysql_db():
    mysql_config_temp = mysql_config.copy()
    database_name = mysql_config_temp.pop("database")

    database_created = mysql_execute(
        f"""
        CREATE DATABASE IF NOT EXISTS `{database_name}`
        CHARACTER SET utf8mb4
        COLLATE utf8mb4_unicode_ci
        """,
        connection=mysql_config_temp,
    )
    if not database_created:
        return False

    return mysql_execute(
        """
        CREATE TABLE IF NOT EXISTS testtable (
            id INT AUTO_INCREMENT PRIMARY KEY,
            value1 INT NULL,
            value2 VARCHAR(255) NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        connection=mysql_config,
    )


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
        created = init_sqlite_db()
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

    # Test SQLITE Default connection
    configure(default_sqlprovider="SQLITE", sqlite_db_path="test_sqlite.db")  # Change to "MYSQL" to test MySQL
    sqlite_test_functions()

    # Test MYSQL Default connection
    # configure(default_sqlprovider="MYSQL", mysql_connection=db_config.mysql_config)  # Change to "MYSQL" to test MySQL
    # mysql_test_functions()

    # create_db_and_run_tests()
    # run_select_queries()
