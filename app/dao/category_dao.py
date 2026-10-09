from mysql.connector import MySQLConnection

from app.models import Category


class CategoryDAO:
    def get_all(self, connection: MySQLConnection) -> list[Category]:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id, nombre_categoria AS name "
                "FROM categorias ORDER BY nombre_categoria"
            )
            return [Category.model_validate(row) for row in cursor.fetchall()]
        finally:
            cursor.close()

    def exists(
        self, connection: MySQLConnection, category_id: int
    ) -> bool:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id FROM categorias WHERE id = %s",
                (category_id,),
            )
            return cursor.fetchone() is not None
        finally:
            cursor.close()
