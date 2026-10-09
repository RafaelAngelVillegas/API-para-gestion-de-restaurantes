from app.models import Category


class CategoryDAO:
    def __init__(self) -> None:
        self._categories = [
            Category(id=1, name="Entrantes"),
            Category(id=2, name="Principales"),
            Category(id=3, name="Postres"),
        ]

    def get_all(self) -> list[Category]:
        return self._categories.copy()

    def exists(self, category_id: int) -> bool:
        return any(category.id == category_id for category in self._categories)
