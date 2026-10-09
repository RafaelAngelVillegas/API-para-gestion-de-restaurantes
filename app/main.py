from fastapi import Depends, FastAPI, HTTPException, Path, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from mysql.connector import MySQLConnection

from app.dao import CategoryDAO, ProductDAO, TableDAO
from app.models import Category, Presentation, Product, RestaurantTable
from app.utils.database_connection import get_database_connection

app = FastAPI(
    title="API restaurante",
    description="Servicio inicial para explorar la carta y las mesas.",
    version="0.1.0",
)

category_dao = CategoryDAO()
product_dao = ProductDAO()
table_dao = TableDAO()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, error: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "detail": "La entrada no es válida. Comprueba los parámetros "
            "y vuelve a intentarlo."
        },
    )


@app.get("/health", tags=["Health"])
def get_health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/categories", response_model=list[Category], tags=["Categories"])
def get_categories(
    connection: MySQLConnection = Depends(get_database_connection),
) -> list[Category]:
    return category_dao.get_all(connection)


@app.get("/tables", response_model=list[RestaurantTable], tags=["Tables"])
def get_tables(
    connection: MySQLConnection = Depends(get_database_connection),
) -> list[RestaurantTable]:
    return table_dao.get_all(connection)


@app.get(
    "/categories/{category_id}/products",
    response_model=list[Product],
    tags=["Products"],
)
def get_products_by_category(
    category_id: int = Path(gt=0, description="Identificador positivo"),
    connection: MySQLConnection = Depends(get_database_connection),
) -> list[Product]:
    if not category_dao.exists(connection, category_id):
        raise HTTPException(
            status_code=404,
            detail=f"No existe la categoría con id {category_id}.",
        )
    return product_dao.get_by_category(connection, category_id)


@app.get(
    "/products/{product_id}/presentations",
    response_model=list[Presentation],
    tags=["Presentations"],
)
def get_product_presentations(
    product_id: int = Path(gt=0, description="Identificador positivo"),
    connection: MySQLConnection = Depends(get_database_connection),
) -> list[Presentation]:
    if product_dao.get_by_id(connection, product_id) is None:
        raise HTTPException(
            status_code=404,
            detail=f"No existe el producto con id {product_id}.",
        )
    return product_dao.get_presentations(connection, product_id)


@app.get(
    "/products/{product_id}",
    response_model=Product,
    tags=["Products"],
)
def get_product(
    product_id: int = Path(gt=0, description="Identificador positivo"),
    connection: MySQLConnection = Depends(get_database_connection),
) -> Product:
    product = product_dao.get_by_id(connection, product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"No existe el producto con id {product_id}.",
        )
    return product
