from pathlib import Path
from typing import Any

# Supported values: "MYSQL", "SQLITE"
DEFAULT_SQL_PROVIDER = "SQLITE"

# SQLITE_DB_PATH = str(Path.cwd() / "test_sqlite.db")
SQLITE_DB_PATH = "test_sqlite.db"

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

    target_provider = DEFAULT_SQL_PROVIDER
    if default_sqlprovider is not None:
        normalized = default_sqlprovider.strip().upper()
        if normalized not in {"MYSQL", "SQLITE"}:
            raise ValueError("default_sqlprovider must be 'MYSQL' or 'SQLITE'")
        target_provider = normalized

    if target_provider == "SQLITE":
        if sqlite_db_path is None:
            raise ValueError("sqlite_db_path is required when default_sqlprovider is 'SQLITE'")
        if not isinstance(sqlite_db_path, str):
            raise TypeError("sqlite_db_path must be a string path")
        if not sqlite_db_path.strip():
            raise ValueError("sqlite_db_path cannot be empty")

    if target_provider == "MYSQL":
        if mysql_connection is None:
            raise ValueError("mysql_connection is required when default_sqlprovider is 'MYSQL'")
        if not isinstance(mysql_connection, dict):
            raise TypeError("mysql_connection must be a dictionary")

    DEFAULT_SQL_PROVIDER = target_provider

    if sqlite_db_path is not None:
        SQLITE_DB_PATH = sqlite_db_path

    if mysql_connection is not None:
        mysql_config = mysql_connection.copy()
