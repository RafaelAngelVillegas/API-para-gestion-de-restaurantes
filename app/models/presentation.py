from pydantic import BaseModel, Field


class Presentation(BaseModel):
    id: int = Field(gt=0)
    name: str
