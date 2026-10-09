from mysql.connector import MySQLConnection

from app.models import RestaurantTable


class TableDAO:
    def get_all(self, connection: MySQLConnection) -> list[RestaurantTable]:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id, nombre_mesa AS name FROM mesas "
                "WHERE nombre_mesa = %s",
                ("Mesa 02",),
            )
            return [
                RestaurantTable.model_validate(row)
                for row in cursor.fetchall()
            ]
        finally:
            cursor.close()
