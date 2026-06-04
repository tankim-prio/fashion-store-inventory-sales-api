from fastapi import FastAPI

from app.database import Base, engine
from app.models import category
from app.routers import categories

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fashion Store Inventory API",
    description="Backend API for fashion store inventory, sales, orders, payments and reports.",
    version="1.0.0"
)

app.include_router(categories.router)


@app.get("/")
def home():
    return {
        "message": "Fashion Store Inventory API is running successfully"
    }
