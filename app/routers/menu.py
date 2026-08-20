from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database.connection import get_db
from models.menu_item import MenuItem
from schemas.menu_item import (
    MenuItemCreate,
    MenuItemResponse
)


router = APIRouter(
    prefix="/menu",
    tags=["Menu"]
)


@router.post(
    "/",
    response_model=MenuItemResponse
)
def create_menu_item(
    item: MenuItemCreate,
    db: Session = Depends(get_db)
):

    new_item = MenuItem(
        name=item.name,
        description=item.description,
        price=item.price,
        image=item.image,
        category_id=item.category_id
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


@router.get(
    "/",
    response_model=list[MenuItemResponse]
)
def get_menu(
    db: Session = Depends(get_db)
):

    return db.query(MenuItem).filter(
        MenuItem.available == True
    ).all()


@router.get(
    "/{item_id}",
    response_model=MenuItemResponse
)
def get_menu_item(
    item_id: int,
    db: Session = Depends(get_db)
):

    item = db.query(MenuItem).filter(
        MenuItem.id == item_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

    return item
