from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int


class OrderCreate(BaseModel):
    customer_name: str
    phone: str | None = None
    table_number: str | None = None
    items: list[OrderItemCreate]


class OrderResponse(BaseModel):
    id: int
    customer_name: str
    phone: str | None
    table_number: str | None
    total_amount: float
    status: str

    class Config:
        from_attributes = True
