from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    sku: Optional[str] = None
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)


class Product(ProductBase):
    id: int
    created_at: datetime


class ClientBase(BaseModel):
    name: str
    address: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None


class OrderItemResponse(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price_at_order: float
    product: Product


class OrderBase(BaseModel):
    client_id: int
    status: str = "new"
    shipping_address: Optional[str] = None
    total_amount: float = 0.0


class OrderResponse(OrderBase):
    id: int
    order_date: datetime
    items: List[OrderItemResponse] = []


class AddItemToOrder(BaseModel):
    order_id: int | None = None
    product_id: int
    quantity: int = Field(gt=0)
