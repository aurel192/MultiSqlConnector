"""Prove configure_db_connection and set_custom_placeholder take effect at runtime."""

import tempfile
import unittest
from pathlib import Path

from multisqlconnector import (
    configure_db_connection,
    get_database_name,
    get_database_provider,
    set_custom_placeholder,
    sql_execute,
    sql_insert,
    sql_select,
    sql_select_named,
)


CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS testtable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value1 INTEGER NULL,
    value2 TEXT NULL
)
"""


class ConfigureBindingTests(unittest.TestCase):
    def tearDown(self) -> None:
        set_custom_placeholder(":param:")

    def test_switching_sqlite_files_uses_live_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_a = str(Path(tmp) / "a.db")
            db_b = str(Path(tmp) / "b.db")

            configure_db_connection(default_sqlprovider="SQLITE", sqlite_db_path=db_a)
            sql_execute(CREATE_TABLE)
            sql_insert(
                "INSERT INTO testtable (value1, value2) VALUES (%p, %p)",
                parameters=(1, "alpha"),
            )
            self.assertEqual(get_database_provider(), "sqlite")
            self.assertEqual(get_database_name(), db_a)
            self.assertEqual(
                sql_select("SELECT value2 FROM testtable WHERE value1 = %p", parameters=(1,)),
                [("alpha",)],
            )

            configure_db_connection(default_sqlprovider="SQLITE", sqlite_db_path=db_b)
            sql_execute(CREATE_TABLE)
            sql_insert(
                "INSERT INTO testtable (value1, value2) VALUES (%p, %p)",
                parameters=(2, "beta"),
            )
            self.assertEqual(get_database_name(), db_b)
            self.assertEqual(
                sql_select("SELECT value2 FROM testtable WHERE value1 = %p", parameters=(2,)),
                [("beta",)],
            )
            self.assertEqual(
                sql_select("SELECT value2 FROM testtable WHERE value1 = %p", parameters=(1,)),
                [],
            )

            configure_db_connection(default_sqlprovider="SQLITE", sqlite_db_path=db_a)
            self.assertEqual(
                sql_select_named(
                    "SELECT value2 FROM testtable WHERE value1 = :param:",
                    parameters=(1,),
                ),
                [{"value2": "alpha"}],
            )

    def test_custom_placeholder_is_read_on_each_query(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = str(Path(tmp) / "placeholders.db")
            configure_db_connection(default_sqlprovider="SQLITE", sqlite_db_path=db_path)
            sql_execute(CREATE_TABLE)
            sql_insert(
                "INSERT INTO testtable (value1, value2) VALUES (%p, %p)",
                parameters=(7, "seven"),
            )

            set_custom_placeholder("@@")
            rows = sql_select(
                "SELECT value2 FROM testtable WHERE value1 = @@",
                parameters=(7,),
            )
            self.assertEqual(rows, [("seven",)])


if __name__ == "__main__":
    unittest.main()


"""
To run this test, use the following command in PowerShell:
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -m unittest tests.test_configure_binding -v
"""
