from sqlalchemy.orm import Session
from ..models.order import Order, OrderStatus
from ..models.unit import Unit, UnitStatus
from typing import List, Optional, Dict
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class OrderManager:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order: Order) -> Order:
        """Create a new order"""
        # Verify product availability
        for product_id, quantity in order.products.items():
            available_units = (
                self.db.query(Unit)
                .filter(Unit.product_id == product_id)
                .filter(Unit.status == UnitStatus.AVAILABLE)
                .count()
            )
            if available_units < quantity:
                raise ValueError(f"Insufficient units available for product {product_id}")

        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_order(self, order_id: str) -> Optional[Order]:
        """Get order by ID"""
        return self.db.query(Order).filter(Order.order_id == order_id).first()

    def process_order(self, order_id: str) -> bool:
        """Process an order"""
        order = self.get_order(order_id)
        if not order or order.status != OrderStatus.PENDING:
            return False

        try:
            # Start transaction
            order.status = OrderStatus.PROCESSING
            
            # Reserve units
            for product_id, quantity in order.products.items():
                units = (
                    self.db.query(Unit)
                    .filter(Unit.product_id == product_id)
                    .filter(Unit.status == UnitStatus.AVAILABLE)
                    .limit(quantity)
                    .all()
                )
                
                if len(units) < quantity:
                    raise ValueError(f"Insufficient units for product {product_id}")
                    
                for unit in units:
                    unit.status = UnitStatus.RESERVED

            # Update order status
            order.status = OrderStatus.SHIPPED
            
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error processing order {order_id}: {str(e)}")
            order.status = OrderStatus.CANCELLED
            self.db.commit()
            return False

    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order"""
        order = self.get_order(order_id)
        if not order or order.status not in {OrderStatus.PENDING, OrderStatus.PROCESSING}:
            return False

        try:
            # Release any reserved units
            reserved_units = (
                self.db.query(Unit)
                .filter(Unit.status == UnitStatus.RESERVED)
                .all()
            )
            
            for unit in reserved_units:
                unit.status = UnitStatus.AVAILABLE

            order.status = OrderStatus.CANCELLED
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error cancelling order {order_id}: {str(e)}")
            return False

    def list_orders(self, status: Optional[OrderStatus] = None) -> List[Order]:
        """List orders, optionally filtered by status"""
        query = self.db.query(Order)
        if status:
            query = query.filter(Order.status == status)
        return query.all()

    def get_order_history(self, customer_id: str) -> List[Order]:
        """Get order history for a customer"""
        return (
            self.db.query(Order)
            .filter(Order.customer_id == customer_id)
            .order_by(Order.order_id.desc())
            .all()
        ) 