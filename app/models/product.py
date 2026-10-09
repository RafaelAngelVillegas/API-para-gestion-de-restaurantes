from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int = Field(gt=0)
    name: str
    category_id: int = Field(gt=0)
