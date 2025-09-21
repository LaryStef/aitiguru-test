from typing import List, Optional
from sqlalchemy import Text, NUMERIC, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "categories"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    
    descendants: Mapped[List["CategoryClosure"]] = relationship(
        primaryjoin="Category.id==CategoryClosure.ancestor_id",
        back_populates="ancestor"
    )
    ancestors: Mapped[List["CategoryClosure"]] = relationship(
        primaryjoin="Category.id==CategoryClosure.descendant_id",
        back_populates="descendant"
    )
    products: Mapped[List["Product"]] = relationship(
        secondary="product_categories",
        back_populates="categories"
    )


class CategoryClosure(Base):
    __tablename__ = "category_closure"
    
    ancestor_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True)
    descendant_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True)
    depth: Mapped[int] = mapped_column(Integer, nullable=False)
    
    ancestor: Mapped["Category"] = relationship(
        primaryjoin="CategoryClosure.ancestor_id==Category.id",
        back_populates="descendants"
    )
    descendant: Mapped["Category"] = relationship(
        primaryjoin="CategoryClosure.descendant_id==Category.id",
        back_populates="ancestors"
    )


class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sku: Mapped[Optional[str]] = mapped_column(Text, unique=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    price: Mapped[float] = mapped_column(NUMERIC(12, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    
    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="product")
    categories: Mapped[List["Category"]] = relationship(
        secondary="product_categories",
        back_populates="products"
    )


class ProductCategory(Base):
    __tablename__ = "product_categories"
    
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True)
    

class Client(Base):
    __tablename__ = "clients"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    contact_phone: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    contact_email: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    
    orders: Mapped[List["Order"]] = relationship(back_populates="client")


class Order(Base):
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    order_date: Mapped[datetime] = mapped_column(default=datetime.now)
    status: Mapped[str] = mapped_column(Text, default="new", nullable=False)
    total_amount: Mapped[float] = mapped_column(NUMERIC(12, 2), default=0, nullable=False)
    shipping_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    client: Mapped["Client"] = relationship(back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"
    
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_at_order: Mapped[float] = mapped_column(NUMERIC(12, 2), nullable=False)
    
    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship(back_populates="order_items")
