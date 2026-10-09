from pydantic import BaseModel, Field


class Category(BaseModel):
    id: int = Field(gt=0)
    name: str
