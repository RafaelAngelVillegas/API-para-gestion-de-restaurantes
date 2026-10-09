from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_reports_api_status() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_categories_returns_examples() -> None:
    response = client.get("/categories")

    assert response.status_code == 200
    assert [category["name"] for category in response.json()] == [
        "Entrantes",
        "Principales",
        "Postres",
    ]


def test_tables_returns_only_table_two() -> None:
    response = client.get("/tables")

    assert response.status_code == 200
    assert response.json() == [{"id": 2, "name": "Mesa 2"}]


def test_products_returns_category_products() -> None:
    response = client.get("/categories/1/products")

    assert response.status_code == 200
    assert [product["name"] for product in response.json()] == [
        "Ensaladilla",
        "Croquetas",
    ]


def test_invalid_category_id_returns_clear_error() -> None:
    response = client.get("/categories/not-an-id/products")

    assert response.status_code == 422
    assert "La entrada no es válida" in response.json()["detail"]


def test_unknown_category_returns_not_found() -> None:
    response = client.get("/categories/99/products")

    assert response.status_code == 404
    assert response.json()["detail"] == "No existe la categoría con id 99."


def test_openapi_docs_are_available() -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/categories/{category_id}/products" in response.json()["paths"]
