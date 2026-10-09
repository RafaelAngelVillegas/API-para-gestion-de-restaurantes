from pydantic import BaseModel, Field


class RestaurantTable(BaseModel):
    id: int = Field(gt=0)
    name: str
