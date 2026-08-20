from pydantic import BaseModel


class MenuItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    image: str | None = None
    category_id: int


class MenuItemResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    image: str | None
    available: bool
    category_id: int

    class Config:
        from_attributes = True
