from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database.connection import get_db

from models.order import Order
from models.order_item import OrderItem
from models.menu_item import MenuItem

from schemas.order import (
    OrderCreate,
    OrderResponse
)


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post(
    "/",
    response_model=OrderResponse
)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):

    total = 0

    new_order = Order(
        customer_name=order_data.customer_name,
        phone=order_data.phone,
        table_number=order_data.table_number,
        total_amount=0,
        status="Pending"
    )

    db.add(new_order)
    db.flush()

    for item in order_data.items:

        menu_item = db.query(MenuItem).filter(
            MenuItem.id == item.menu_item_id
        ).first()

        if not menu_item:
            raise HTTPException(
                status_code=404,
                detail=f"Menu item {item.menu_item_id} not found"
            )

        if not menu_item.available:
            raise HTTPException(
                status_code=400,
                detail=f"{menu_item.name} is not available"
            )

        item_total = (
            menu_item.price *
            item.quantity
        )

        total += item_total

        order_item = OrderItem(
            order_id=new_order.id,
            menu_item_id=menu_item.id,
            quantity=item.quantity,
            price=menu_item.price
        )

        db.add(order_item)

    new_order.total_amount = total

    db.commit()
    db.refresh(new_order)

    return new_order


@router.get(
    "/",
    response_model=list[OrderResponse]
)
def get_orders(
    db: Session = Depends(get_db)
):

    return db.query(Order).all()
