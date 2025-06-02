import mysql.connector
import psycopg2
from mysql.connector import Error as MySQLError
from psycopg2 import Error as PostgreSQLError
from config import get_db_config
from contextlib import contextmanager

def create_connection(config):
    if config.pop('engine') == 'postgresql':
        return psycopg2.connect(**config)
    else:
        return mysql.connector.connect(**config)

@contextmanager
def get_connection():
    connection = None
    try:
        config = get_db_config()
        connection = create_connection(config)
        yield connection
    finally:
        if connection:
            try:
                connection.close()
            except (MySQLError, PostgreSQLError):
                pass

@contextmanager
def get_cursor(dictionary=False):
    with get_connection() as conn:
        if isinstance(conn, psycopg2.extensions.connection):
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor if dictionary else None)
        else:
            cursor = conn.cursor(dictionary=dictionary)
        try:
            yield cursor, conn
        finally:
            cursor.close() 