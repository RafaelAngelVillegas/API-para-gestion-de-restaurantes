from mysql.connector import MySQLConnection, connect

from collections.abc import Generator

from fastapi import HTTPException
from mysql.connector import Error, MySQLConnection, connect

from app.utils.environment import get_mysql_config


class DatabaseConnection:
    def __init__(self) -> None:
        self._connection: MySQLConnection | None = None

    def open(self) -> MySQLConnection:
        if self._connection is not None and self._connection.is_connected():
            return self._connection

        self._connection = connect(**get_mysql_config(), connection_timeout=5)
        return self._connection

    def close(self) -> None:
        if self._connection is not None and self._connection.is_connected():
            self._connection.close()
        self._connection = None


def get_database_connection() -> Generator[MySQLConnection, None, None]:
    database = DatabaseConnection()
    try:
        yield database.open()
    except Error as error:
        raise HTTPException(
            status_code=503,
            detail="No se pudo consultar la base de datos. Inténtalo de nuevo.",
        ) from error
    finally:
        database.close()
