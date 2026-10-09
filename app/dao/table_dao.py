from app.models import RestaurantTable


class TableDAO:
    def __init__(self) -> None:
        self._tables = [
            RestaurantTable(id=2, name="Mesa 2"),
        ]

    def get_all(self) -> list[RestaurantTable]:
        return self._tables.copy()
