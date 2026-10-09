from app.models import Order


class OrderDAO:
    def __init__(self) -> None:
        self._orders: list[Order] = []

    def get_all(self) -> list[Order]:
        return self._orders.copy()
