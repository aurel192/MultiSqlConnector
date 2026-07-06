from pathlib import Path
import sys

# Allow direct execution: py src/multisqlconnector/example.py
if __package__ is None or __package__ == "":
    src_root = Path(__file__).resolve().parents[1]
    if str(src_root) not in sys.path:
        sys.path.insert(0, str(src_root))

from multisqlconnector import sql_select, sql_select_cast, sql_select_named, sql_execute, sql_insert, sql_update, sql_delete,sql_select_cast, sql_select_named
from multisqlconnector import db_config
from multisqlconnector.db_config import mysql_config, SQLITE_DB_PATH, DEFAULT_SQL_PROVIDER, configure as configure_db_connection, set_custom_placeholder
from multisqlconnector.mysqlhelper import mysql_execute, mysql_test_functions, init_mysql_db
from multisqlconnector.sqlite3helper import *


def create_db_and_run_tests():
    current_provider = db_config.DEFAULT_SQL_PROVIDER
    current_db = db_config.SQLITE_DB_PATH if current_provider == "SQLITE" else db_config.mysql_config.get("database", "Unknown")
    print(f"-------- RUNNING TESTS USING: {current_provider} (Database: {current_db}) ---------------------")
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
    db_name = db_config.SQLITE_DB_PATH if current_provider == "SQLITE" else db_config.mysql_config.get("database", "Unknown")
    print(f"-------- RUNNING SELECT QUERIES ON {current_provider} Database: {db_name} --------")
    print(f"--------  WITHOUT CASTING --------")
    result = sql_select(
        sqlquery="SELECT id, value1, value2 FROM testtable WHERE id > %p",
        parameters=(2,)
    )

    print(f"Not casted rows: {result}\n")
    for row in result:
        print(f"Row ID: {row[0]}")  # type: ignore[index]
        print(f"Row: {row}")

    print(f"--------  WITH CASTING --------")
    casted_rows = sql_select_cast(
        "SELECT id, value1, value2 FROM testtable WHERE id > %p",
        result_types=(int, int, str),
        parameters=(2,)
    )

    print(f"Casted rows: {casted_rows}\n")
    for row in casted_rows:
        print(f"Row ID: {row[0]}")  # type: ignore[index]
        print(f"Row: {row}")

    print(f"--------  WITH NAMED RESULTS --------")
    named_rows = sql_select_named(
        sqlquery="SELECT id, value1, value2 FROM testtable WHERE id > :param:",
        parameters=(2,)
    )

    print(f"Named rows: {named_rows}\n")
    for row in named_rows:
        print(f"Row ID: {row['id']}")
        print(f"Row: {row}")


def test_function_01():
    sqlite_create_script = f"""
            CREATE TABLE IF NOT EXISTS testtable (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value1 INTEGER NULL,
                value2 TEXT NULL
            )
            """

    # Test Sqlite3 connection
    configure_db_connection(default_sqlprovider="SQLITE", sqlite_db_path="test_sqlite.db")
    created = init_sqlite_db(createscript=sqlite_create_script)
    print(f"SQLite database {db_config.SQLITE_DB_PATH} created: {created} (or it already existed)")
    sqlite_test_functions()

    configure_db_connection(default_sqlprovider="SQLITE", sqlite_db_path="something_else_sqlite.db")
    created = init_sqlite_db(createscript=sqlite_create_script)
    print(f"SQLite database {db_config.SQLITE_DB_PATH} created with custom connection: {created} (or it already existed)")
    create_db_and_run_tests()

    # Test MYSQL and Sqlite connections by switching between them
    configure_db_connection(default_sqlprovider="MYSQL", mysql_connection=mysql_config)
    mysql_test_functions()

    configure_db_connection(default_sqlprovider="SQLITE", sqlite_db_path="test_sqlite.db")
    sqlite_test_functions()

    configure_db_connection(default_sqlprovider="MYSQL")
    mysql_test_functions()

    sqlite_test_functions("something_else_sqlite.db")


def test_function_02():
    # Test MYSQL connections
    configure_db_connection(default_sqlprovider="MYSQL", mysql_connection=db_config.mysql_config)
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

    # Test MYSQL with custom connection settings
    configure_db_connection(default_sqlprovider="MYSQL", mysql_connection=custom_mysql_settings)
    # This will create the database if it doesn't exist. Database name = test_db_02
    init_mysql_db(connection=custom_mysql_settings)
    create_db_and_run_tests()


    print("\n\n==================== Running SELECT Queries on both MySQL and SQLite databases ====================")
    
    set_custom_placeholder(":param:") 

    configure_db_connection(default_sqlprovider="MYSQL")
    run_select_queries()

    configure_db_connection(default_sqlprovider="SQLITE")
    run_select_queries()


def create_sqlite_testdb():
    sql_files_path = Path(__file__).resolve().parent / "etc"
    configure_db_connection(default_sqlprovider="SQLITE", sqlite_db_path="testdb_sqlite_192.db")

    # try:
    #     sqlite_create_script_path = sql_files_path / "sqlite_test_create.sql"
    #     with open(sqlite_create_script_path, "r", encoding="utf-8") as f:
    #         sqlite_create_script = f.read()

    #     sql_execute(sqlquery=sqlite_create_script)
    # except Exception as e:
    #     print(f"Error creating SQLite test database: {e}")

    # try:
    #     sqlite_insert_script_path = sql_files_path / "sqlite_test_insert.sql"
    #     with open(sqlite_insert_script_path, "r", encoding="utf-8") as f:
    #         sqlite_insert_script = f.read()

    #     sql_execute(sqlquery=sqlite_insert_script)
    # except Exception as e:
    #     print(f"Error creating SQLite test database: {e}")

    try:
        sqlite_create_and_insert_script_path = sql_files_path / "sqlite_test_create_and_insert.sql"
        with open(sqlite_create_and_insert_script_path, "r", encoding="utf-8") as f:
            sqlite_create_and_insert_script = f.read()

        sql_execute(sqlquery=sqlite_create_and_insert_script)
    except Exception as e:
        print(f"Error creating SQLite test database: {e}")


def create_mysql_testdb():
    sql_files_path = Path(__file__).resolve().parent / "etc"
    configure_db_connection(default_sqlprovider="MYSQL", mysql_connection=db_config.mysql_config_02)

    try:
        mysql_create_script_path = sql_files_path / "mysql_test_db_02_create.sql"
        with open(mysql_create_script_path, "r", encoding="utf-8") as f:
            mysql_create_script = f.read()

        sql_execute(sqlquery=mysql_create_script)
    except Exception as e:
        print(f"Error creating MySQL test database: {e}")

    try:
        mysql_insert_script_path = sql_files_path / "mysql_test_db_02_insert.sql"
        with open(mysql_insert_script_path, "r", encoding="utf-8") as f:
            mysql_insert_script = f.read()

        sql_execute(sqlquery=mysql_insert_script)
    except Exception as e:
        print(f"Error inserting data into MySQL test database: {e}")


if __name__ == "__main__":

    # clear screen
    print("\033[2J\033[H", end="")

    create_sqlite_testdb()
    # sqlite_test_functions()

    # create_db_and_run_tests()

    # create_mysql_testdb()

    # test_function_01()

    # test_function_02()
