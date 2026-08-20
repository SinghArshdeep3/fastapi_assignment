from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime
)

from sqlalchemy.orm import relationship

from app.database.connection import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_name = Column(
        String(100),
        nullable=False
    )

    phone = Column(
        String(20)
    )

    table_number = Column(
        String(20)
    )

    total_amount = Column(
        Float,
        nullable=False
    )

    status = Column(
        String(30),
        default="Pending"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    items = relationship(
        "OrderItem",
        back_populates="order"
    )
