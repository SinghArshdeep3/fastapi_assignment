from fastapi import FastAPI

from app.database.connection import Base, engine

import app.models

from app.routers import categories
from app.routers import menu
from app.routers import orders


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Digital Menu",
    description="Restaurant Digital Menu and Online Ordering System",
    version="1.0.0"
)


app.include_router(categories.router)
app.include_router(menu.router)
app.include_router(orders.router)


@app.get("/")
def home():
    return {
        "message": "Digital Menu API is running"
    }
