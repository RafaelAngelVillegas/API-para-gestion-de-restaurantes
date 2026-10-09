from app.models import Product


class ProductDAO:
    def __init__(self) -> None:
        self._products = [
            Product(id=1, name="Ensaladilla", category_id=1),
            Product(id=2, name="Croquetas", category_id=1),
            Product(id=3, name="Paella", category_id=2),
            Product(id=4, name="Flan", category_id=3),
        ]

    def get_by_category(self, category_id: int) -> list[Product]:
        return [
            product
            for product in self._products
            if product.category_id == category_id
        ]
