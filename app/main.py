from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.dao import CategoryDAO, ProductDAO, TableDAO
from app.models import Category, Product, RestaurantTable

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
def get_categories() -> list[Category]:
    return category_dao.get_all()


@app.get("/tables", response_model=list[RestaurantTable], tags=["Tables"])
def get_tables() -> list[RestaurantTable]:
    return table_dao.get_all()


@app.get(
    "/categories/{category_id}/products",
    response_model=list[Product],
    tags=["Products"],
)
def get_products_by_category(
    category_id: int = Path(gt=0, description="Identificador positivo"),
) -> list[Product]:
    if not category_dao.exists(category_id):
        raise HTTPException(
            status_code=404,
            detail=f"No existe la categoría con id {category_id}.",
        )
    return product_dao.get_by_category(category_id)
