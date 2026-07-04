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
from multisqlconnector import DEFAULT_SQL_PROVIDER, configure, sql_insert, sql_select, sql_update, sql_delete, sql_execute

print(DEFAULT_SQL_PROVIDER)  # "SQLITE" by default
```

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

## SQLite usage

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

- `%p` (recommended)
- `?p`
- `:p`
- `:param`

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
