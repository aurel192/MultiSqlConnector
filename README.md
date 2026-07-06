# multisqlconnector

Simple SQL wrapper helpers for MySQL/MariaDB and SQLite.

![multisqlconnector](dry.png)

[GitHub - aurel192 / MultiSqlConnector](https://github.com/aurel192/MultiSqlConnector)

## Install

From TestPyPI:

```bash
py -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple multisqlconnector-aurel192
```

From source:

```bash
py -m pip install .
```

## Quick start

```python
from multisqlconnector import DEFAULT_SQL_PROVIDER, configure, sql_insert, sql_select, sql_select_named, sql_update, sql_delete, sql_execute

custom_mysql_settings: dict[str, Any] = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "1234",
    "database": "my_mysql_database",
    "charset": "utf8mb4",
    "collation": "utf8mb4_unicode_ci",
}

# Test MYSQL with custom connection settings
configure_db_connection(default_sqlprovider="MYSQL", mysql_connection=custom_mysql_settings)

with open("create_and_insert_script.sql", "r", encoding="utf-8") as file:
    create_and_insert_script = file.read()

sql_execute(sqlquery=create_and_insert_script)

set_custom_placeholder(":param:")

named_rows = sql_select_named(
    sqlquery="SELECT id, value1, value2 FROM testtable WHERE id >= :param: AND id <= :param:",
    parameters=(1, 100, )
)

for row in named_rows:
    print(f"Row ID: {row['id']}")
    print(f"Row: {row}")
```

## Switch database engines and databases on the fly without a wall of text

The main goal of this package is to let you switch quickly between SQLite and MySQL,
and also switch to different database files or schemas, without rewriting your query code.

With `configure(...)`, you can:

- use the same functions for different sql database systems!
- modify which database to connect with one simple function call. So you can use multiple databases and database engines
- change SQL engines at runtime (`SQLITE` <-> `MYSQL`) (`MsSQL` and `PostgreSQL` soon...)
- swap SQLite database files (for example `test_sqlite.db` and `something_else_sqlite.db`)
- swap MySQL connection settings (for example `test_db_01` and `test_db_02`)
- keep using the same helper functions (`sql_select`, `sql_insert`, `sql_update`, `sql_delete`, `sql_execute`) for different systems

## MySQL usage
```python
configure(
    default_sqlprovider="MYSQL",
    mysql_connection={
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "your-password",
        "database": "test_db",
        "charset": "utf8mb4",
        "collation": "utf8mb4_unicode_ci",
    },
)

sql_insert(
    "INSERT INTO testtable (value1, value2) VALUES (%p, %p)",
    parameters=(42, "hello"),
)

rows = sql_select(
    "SELECT id, value1, value2 FROM testtable WHERE id > %p",
    parameters=(0,),
)

for row in rows:
    print(row)

rows = sql_select_named(
    "SELECT id, value1, value2 FROM testtable WHERE id > %p",
    parameters=(0,),
)

for row in rows:
    print(row)
```

## SQLite3 usage

```python
from multisqlconnector import configure, sql_execute, sql_select_named

configure(sqlprovider="SQLITE", sqlite_db_path="./example.db")

sql_execute(
    """
    CREATE TABLE IF NOT EXISTS testtable (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        value1 INTEGER NULL,
        value2 TEXT NULL
    )
    """
)

sql_insert(
    "INSERT INTO testtable (value1, value2) VALUES (%p, %p)",
    parameters=(42, "hello"),
)

rows = sql_select_named("SELECT id, value1, value2 FROM testtable WHERE id > %p", parameters=(0,))
for row in rows:
    print(row)
```

## Placeholders

Use portable placeholders in queries:

- `:param:` (recommended)
- `%p`
- `?p`
- `:p`

Using parameters will prevent againts sql injections!


The package normalizes them automatically:

- MySQL/MariaDB: `%s`
- SQLite: `?`

## Demo script

Run the packaged demo module:

```bash
py -m multisqlconnector.example
```

## Build and upload

```bash
py -m pip install --upgrade build twine
py -m build
py -m twine check dist/*
py -m twine upload --repository testpypi dist/*
```
