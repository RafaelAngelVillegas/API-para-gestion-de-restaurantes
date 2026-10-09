from mysql.connector import MySQLConnection

from app.models import Product
from app.models.presentation import Presentation


class ProductDAO:
    def get_by_category(
        self, connection: MySQLConnection, category_id: int
    ) -> list[Product]:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id, producto AS name, id_categoria AS category_id "
                "FROM carta WHERE id_categoria = %s ORDER BY producto",
                (category_id,),
            )
            return [Product.model_validate(row) for row in cursor.fetchall()]
        finally:
            cursor.close()

    def get_by_id(
        self, connection: MySQLConnection, product_id: int
    ) -> Product | None:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id, producto AS name, "
                "id_categoria AS category_id "
                "FROM carta WHERE id = %s",
                (product_id,),
            )
            row = cursor.fetchone()
            return Product.model_validate(row) if row is not None else None
        finally:
            cursor.close()

    def get_presentations(
        self, connection: MySQLConnection, product_id: int
    ) -> list[Presentation]:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT pr.id, pr.nombre_presentacion AS name "
                "FROM carta AS c "
                "JOIN presentaciones AS pr ON ("
                "(pr.nombre_presentacion = 'Unidad' AND c.unidad = 1) OR "
                "(pr.nombre_presentacion = 'Tapa' AND c.tapa = 1) OR "
                "(pr.nombre_presentacion = 'Media Ración' AND c.media = 1) OR "
                "(pr.nombre_presentacion = 'Ración' AND c.racion = 1)"
                ") WHERE c.id = %s ORDER BY pr.id",
                (product_id,),
            )
            return [
                Presentation.model_validate(row) for row in cursor.fetchall()
            ]
        finally:
            cursor.close()
