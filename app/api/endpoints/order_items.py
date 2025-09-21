from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.models import Order, OrderItem, Product
from app.schemas.schemas import AddItemToOrder, OrderResponse

router = APIRouter()


@router.post("/orders/add-item", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def add_item_to_order(
    item_data: AddItemToOrder,
    db: Session = Depends(get_db)
) -> Order:
    """
    Add a product to an order.

    - If the product is already in the order, its quantity will be increased.
    - If there isn't enough stock available, an error will be returned.
    """
    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {item_data.product_id} not found"
        )

    if product.quantity < item_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not enough stock available. Requested: {item_data.quantity}, Available: {product.quantity}"
        )

    order = db.query(Order).filter(Order.id == item_data.order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {item_data.order_id} not found"
        )
    
    from sqlalchemy import and_

    existing_item = db.query(OrderItem).filter(
        and_(
            OrderItem.order_id == item_data.order_id,
            OrderItem.product_id == item_data.product_id
        )
    ).first()

    if existing_item:
        existing_item.quantity += item_data.quantity
        order.total_amount += product.price * item_data.quantity
    else:
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item_data.quantity,
            price_at_order=product.price
        )
        db.add(order_item)
        order.total_amount += product.price * item_data.quantity

    product.quantity -= item_data.quantity    
    db.commit()
    db.refresh(order)
    return order
