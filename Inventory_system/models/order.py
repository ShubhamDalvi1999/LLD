from sqlalchemy import Column, String, Float, JSON, Enum as SQLEnum, event
from sqlalchemy.orm import validates
from enum import Enum
from .database import Base
from typing import Dict

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True)
    customer_id = Column(String, nullable=False)
    products = Column(JSON, nullable=False)  # Dict[str, int] - product_id: quantity
    status = Column(SQLEnum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    total_amount = Column(Float, default=0.0)

    @validates('products')
    def validate_products(self, key, products):
        """Validate products dictionary"""
        if not isinstance(products, dict):
            raise ValueError("Products must be a dictionary")
        if not all(isinstance(k, str) and isinstance(v, int) and v > 0 for k, v in products.items()):
            raise ValueError("Products must be a dictionary of product_id: quantity (positive integer)")
        return products

    @validates('status')
    def validate_status_transition(self, key, status):
        """Validate status transitions"""
        if hasattr(self, 'status'):
            valid_transitions = {
                OrderStatus.PENDING: {OrderStatus.PROCESSING, OrderStatus.CANCELLED},
                OrderStatus.PROCESSING: {OrderStatus.SHIPPED, OrderStatus.CANCELLED},
                OrderStatus.SHIPPED: {OrderStatus.DELIVERED},
                OrderStatus.DELIVERED: set(),  # Terminal state
                OrderStatus.CANCELLED: set()   # Terminal state
            }
            if status not in valid_transitions[self.status]:
                raise ValueError(f"Invalid status transition from {self.status} to {status}")
        return status

    def calculate_total(self, product_prices: Dict[str, float]):
        """Calculate total order amount"""
        self.total_amount = sum(
            quantity * product_prices[prod_id]
            for prod_id, quantity in self.products.items()
        )
        return self.total_amount

    def update_status(self, status: OrderStatus):
        """Update order status with validation"""
        self.status = status  # This will trigger validate_status_transition

    def to_dict(self):
        """Convert order to dictionary"""
        return {
            'order_id': self.order_id,
            'customer_id': self.customer_id,
            'products': self.products,
            'status': self.status.value,
            'total_amount': self.total_amount
        }

# Event listeners for order status changes
@event.listens_for(Order.status, 'set')
def order_status_change(target, value, oldvalue, initiator):
    """Handle order status changes"""
    if oldvalue is None:  # New order
        return
    
    # Emit events based on status change
    if value == OrderStatus.PROCESSING:
        # Reserve units
        pass
    elif value == OrderStatus.SHIPPED:
        # Update unit locations
        pass
    elif value == OrderStatus.DELIVERED:
        # Update inventory
        pass
    elif value == OrderStatus.CANCELLED:
        # Release reserved units
        pass 