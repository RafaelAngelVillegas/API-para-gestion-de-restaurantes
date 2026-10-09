from pydantic import BaseModel, Field


class Order(BaseModel):
    id: int = Field(gt=0)
    table_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    presentation_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
