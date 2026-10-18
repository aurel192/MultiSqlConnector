"""Public API for multisqlconnector."""

from . import db_config
from .db_config import configure_db_connection
from .db_config import get_database_name, get_database_provider
from .db_config import set_custom_placeholder
from .sqlhelper import (
    sql_delete,
    sql_execute,
    sql_insert,
    sql_select,
    sql_select_cast,
    sql_select_named,
    sql_select_named_cast,
    sql_update,
)

__all__ = [
    "configure_db_connection",
    "DEFAULT_SQL_PROVIDER",
    "get_database_name",
    "get_database_provider",
    "set_custom_placeholder",
    "sql_delete",
    "sql_execute",
    "sql_insert",
    "sql_select",
    "sql_select_cast",
    "sql_select_named",
    "sql_select_named_cast",
    "sql_update",
]


def __getattr__(name: str):
    if name == "DEFAULT_SQL_PROVIDER":
        return db_config.DEFAULT_SQL_PROVIDER
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
