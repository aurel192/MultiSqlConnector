from pathlib import Path
from typing import Any

# Supported values: "MYSQL", "SQLITE"
DEFAULT_SQL_PROVIDER = "SQLITE"

# SQLITE_DB_PATH = str(Path.cwd() / "test_sqlite.db")
SQLITE_DB_PATH = "test_sqlite.db"

CUSTOM_PLACEHOLDER = "%p"  # Custom placeholder for parameters in SQL queries

mysql_config: dict[str, Any] = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "1234",
    "database": "test_db",
    "charset": "utf8mb4",
    "collation": "utf8mb4_unicode_ci",
}

mysql_config_02: dict[str, Any] = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "1234",
    "database": "test_db_02",
    "charset": "utf8mb4",
    "collation": "utf8mb4_unicode_ci",
}


def configure(
    *,
    default_sqlprovider: str | None = None,
    sqlite_db_path: str | None = None,
    mysql_connection: dict[str, Any] | None = None,
) -> None:
    """Update package-level defaults without editing installed files."""
    global DEFAULT_SQL_PROVIDER, SQLITE_DB_PATH, mysql_config

    # Set the default SQL provider if provided and valid, otherwise keep the existing default.
    target_sql_provider = DEFAULT_SQL_PROVIDER
    if default_sqlprovider is not None:
        normalized_sql_provider = default_sqlprovider.strip().upper()
        if normalized_sql_provider not in {"MYSQL", "SQLITE"}:
            raise ValueError("default_sqlprovider must be 'MYSQL' or 'SQLITE'")
        target_sql_provider = normalized_sql_provider
        DEFAULT_SQL_PROVIDER = target_sql_provider

    if target_sql_provider == "SQLITE":
        if sqlite_db_path is None and (SQLITE_DB_PATH is None or SQLITE_DB_PATH.strip() == ""):
            raise ValueError("sqlite_db_path is required when default_sqlprovider is 'SQLITE' and sqlite_db_path is not set.")
        if sqlite_db_path is not None and not sqlite_db_path.strip() and (SQLITE_DB_PATH is None or SQLITE_DB_PATH.strip() == ""):
            raise ValueError("sqlite_db_path is required when default_sqlprovider is 'SQLITE' and sqlite_db_path is not set.")

    # Set the sqlite database path based on the provided arguments (sqlite_db_path)
    if sqlite_db_path is not None:
        SQLITE_DB_PATH = sqlite_db_path

    if target_sql_provider == "MYSQL":
        if mysql_connection is None and (mysql_config is None or not isinstance(mysql_config, dict)):
            raise ValueError("mysql_connection is required when default_sqlprovider is 'MYSQL' and mysql_config is not set.")
        if mysql_connection is not None and not isinstance(mysql_connection, dict):
            raise TypeError("mysql_connection must be a dictionary when default_sqlprovider is 'MYSQL'")

    # Set mysql connection settings based on the provided arguments (mysql_connection)
    if mysql_connection is not None:
        mysql_config = mysql_connection.copy()

def set_custom_placeholder(placeholder: str) -> None:
    """Set a custom placeholder for SQL queries."""
    global CUSTOM_PLACEHOLDER
    if not isinstance(placeholder, str) or not placeholder.strip():
        raise ValueError("Custom placeholder must be a non-empty string.")
    CUSTOM_PLACEHOLDER = placeholder.strip()
