import uvicorn
from fastapi import FastAPI
from app.api.endpoints import order_items

app = FastAPI(
    title="Order Management API",
    description="API for managing orders and products",
    version="1.0.0",
)


app.include_router(order_items.router, prefix="/api", tags=["orders"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
