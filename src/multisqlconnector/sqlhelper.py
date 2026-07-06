import re
import sqlite3

import mysql.connector

from . import db_config
from .mysqlhelper import mysql_delete, mysql_execute, mysql_insert, mysql_select, mysql_update
from .sqlite3helper import (
    sqlite_delete,
    sqlite_execute,
    sqlite_insert,
    sqlite_select,
    sqlite_update,
)


def _normalize_query(sqlquery: str) -> str:
    sqlprovider = db_config.DEFAULT_SQL_PROVIDER
    if sqlprovider == "MYSQL":
        sqlquery = sqlquery.replace(db_config.CUSTOM_PLACEHOLDER, "%s")
        sqlquery = sqlquery.replace("%p", "%s")
        sqlquery = sqlquery.replace("?p", "%s")
        sqlquery = sqlquery.replace(":p", "%s")
        sqlquery = sqlquery.replace(":param", "%s")
        return sqlquery

    sqlquery = sqlquery.replace(db_config.CUSTOM_PLACEHOLDER, "?")
    sqlquery = sqlquery.replace("%p", "?")
    sqlquery = sqlquery.replace("?p", "?")
    sqlquery = sqlquery.replace(":p", "?")
    sqlquery = sqlquery.replace(":param", "?")
    return sqlquery

def sql_execute(sqlquery, parameters=None, connection=None):
    query = _normalize_query(sqlquery)
    sqlprovider = db_config.DEFAULT_SQL_PROVIDER
    if sqlprovider == "MYSQL":
        return mysql_execute(query, parameters, connection=connection)
    return sqlite_execute(query, parameters, connection=connection)


def sql_select_cast(sqlquery, result_types, parameters=None, connection=None):
    query = _normalize_query(sqlquery)
    results = sql_select(query, parameters=parameters, connection=connection)

    casted_results = []
    for row in results:
        casted_row = []
        for index, value in enumerate(row):
            if index < len(result_types) and result_types[index] is not None and value is not None:
                casted_row.append(result_types[index](value))
            else:
                casted_row.append(value)
        casted_results.append(tuple(casted_row))

    return casted_results


def sql_select_named(sqlquery, parameters=None, connection=None):
    query = _normalize_query(sqlquery)
    conn = None
    cur = None
    try:
        sqlprovider = db_config.DEFAULT_SQL_PROVIDER
        if sqlprovider == "MYSQL":
            conn_config = db_config.mysql_config if connection is None else connection
            conn = mysql.connector.connect(**conn_config)
            cur = conn.cursor()
        else:
            conn = connection if connection is not None else sqlite3.connect(db_config.SQLITE_DB_PATH)
            cur = conn.cursor()

        if parameters is not None:
            cur.execute(query, parameters)
        else:
            cur.execute(query)

        rows = cur.fetchall()
        columns = [column[0] for column in cur.description] if cur.description else []
        return [dict(zip(columns, row)) for row in rows]
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def sql_select(sqlquery, parameters=None, connection=None):
    query = _normalize_query(sqlquery)
    sqlprovider = db_config.DEFAULT_SQL_PROVIDER
    if sqlprovider == "MYSQL":
        return mysql_select(query, parameters, connection=connection)
    return sqlite_select(query, parameters, connection=connection)


def sql_insert(sqlquery, parameters=None, many: bool = False, connection=None):
    query = _normalize_query(sqlquery)
    sqlprovider = db_config.DEFAULT_SQL_PROVIDER
    if sqlprovider == "MYSQL":
        return mysql_insert(query, parameters, many=many, connection=connection)
    return sqlite_insert(query, parameters, many=many, connection=connection)


def sql_update(sqlquery, parameters=None, connection=None):
    query = _normalize_query(sqlquery)
    sqlprovider = db_config.DEFAULT_SQL_PROVIDER
    if sqlprovider == "MYSQL":
        return mysql_update(query, parameters, connection=connection)
    return sqlite_update(query, parameters, connection=connection)


def sql_delete(sqlquery, parameters=None, connection=None):
    query = _normalize_query(sqlquery)
    sqlprovider = db_config.DEFAULT_SQL_PROVIDER
    if sqlprovider == "MYSQL":
        return mysql_delete(query, parameters, connection=connection)
    return sqlite_delete(query, parameters, connection=connection)
