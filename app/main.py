from fastapi import FastAPI

app = FastAPI(
    title="Fashion Store Inventory API",
    description="Backend API for fashion store inventory, sales, orders, payments and reports.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Fashion Store Inventory API is running successfully"
    }
