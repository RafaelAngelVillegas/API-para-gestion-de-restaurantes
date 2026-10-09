from mysql.connector import MySQLConnection, connect

from app.utils.environment import get_mysql_config


class DatabaseConnection:
    def __init__(self) -> None:
        self._connection: MySQLConnection | None = None

    def open(self) -> MySQLConnection:
        if self._connection is not None and self._connection.is_connected():
            return self._connection

        self._connection = connect(**get_mysql_config())
        return self._connection

    def close(self) -> None:
        if self._connection is not None and self._connection.is_connected():
            self._connection.close()
        self._connection = None
