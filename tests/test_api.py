from collections.abc import Generator
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.utils.database_connection import get_database_connection


class FakeCursor:
    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []
        self.row: dict[str, Any] | None = None
        self.query = ""
        self.params: tuple[Any, ...] = ()

    def execute(
        self, query: str, params: tuple[Any, ...] | None = None
    ) -> None:
        self.query = query
        self.params = params or ()
        if "FROM categorias" in query and "WHERE" in query:
            category_id = self.params[0]
            self.row = {"id": category_id} if category_id in (1, 3) else None
            self.rows = []
        elif "FROM categorias" in query:
            self.rows = [
                {"id": 1, "name": "Bebidas"},
                {"id": 3, "name": "Entrantes"},
            ]
            self.row = None
        elif "FROM mesas" in query:
            self.rows = [{"id": 1093, "name": "Mesa 02"}]
            self.row = None
        elif "JOIN presentaciones" in query:
            self.rows = [
                {"id": 2, "name": "Tapa"},
                {"id": 3, "name": "Media Ración"},
            ]
            self.row = None
        elif "FROM carta" in query and "WHERE id_categoria = %s" in query:
            self.rows = [
                {"id": 10, "name": "Ensaladilla Rusa", "category_id": 3}
            ]
            self.row = None
        elif "FROM carta" in query:
            product_id = self.params[0]
            self.row = (
                {"id": 10, "name": "Ensaladilla Rusa", "category_id": 3}
                if product_id == 10
                else None
            )
            self.rows = []
        else:
            raise AssertionError(f"Consulta inesperada: {query}")

    def fetchall(self) -> list[dict[str, Any]]:
        if "FROM mesas" in self.query:
            assert "WHERE nombre_mesa = %s" in self.query
            assert self.params == ("Mesa 02",)
        return self.rows

    def fetchone(self) -> dict[str, Any] | None:
        return self.row

    def close(self) -> None:
        pass


class FakeConnection:
    def cursor(self, dictionary: bool = False) -> FakeCursor:
        assert dictionary
        return FakeCursor()


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    connection = FakeConnection()

    def override_connection() -> Generator[FakeConnection, None, None]:
        yield connection

    app.dependency_overrides[get_database_connection] = override_connection
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_database_connection, None)


def test_health_reports_api_status(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_categories_returns_database_records(client: TestClient) -> None:
    response = client.get("/categories")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Bebidas"},
        {"id": 3, "name": "Entrantes"},
    ]


def test_tables_only_returns_mesa_02(client: TestClient) -> None:
    response = client.get("/tables")

    assert response.status_code == 200
    assert response.json() == [{"id": 1093, "name": "Mesa 02"}]


def test_products_returns_selected_category(client: TestClient) -> None:
    response = client.get("/categories/3/products")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 10, "name": "Ensaladilla Rusa", "category_id": 3}
    ]


def test_unknown_category_returns_not_found(client: TestClient) -> None:
    response = client.get("/categories/99/products")

    assert response.status_code == 404
    assert response.json()["detail"] == "No existe la categoría con id 99."


def test_invalid_category_id_returns_clear_error(client: TestClient) -> None:
    response = client.get("/categories/not-an-id/products")

    assert response.status_code == 422
    assert "La entrada no es válida" in response.json()["detail"]


def test_product_detail_returns_database_record(client: TestClient) -> None:
    response = client.get("/products/10")

    assert response.status_code == 200
    assert response.json() == {
        "id": 10,
        "name": "Ensaladilla Rusa",
        "category_id": 3,
    }


def test_presentations_only_returns_active_options(
    client: TestClient,
) -> None:
    response = client.get("/products/10/presentations")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 2, "name": "Tapa"},
        {"id": 3, "name": "Media Ración"},
    ]


@pytest.mark.parametrize(
    "path",
    ["/products/99", "/products/99/presentations"],
)
def test_unknown_product_returns_not_found(
    client: TestClient, path: str
) -> None:
    response = client.get(path)

    assert response.status_code == 404
    assert response.json()["detail"] == "No existe el producto con id 99."


def test_openapi_docs_list_menu_endpoints(client: TestClient) -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/tables" in paths
    assert "/categories" in paths
    assert "/categories/{category_id}/products" in paths
    assert "/products/{product_id}/presentations" in paths
    assert "/products/{product_id}" in paths
