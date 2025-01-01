from dataclasses import dataclass
from enum import Enum
from typing import Dict

class OrderStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

@dataclass
class Order:
    order_id: str
    customer_id: str
    products: Dict[str, int]  # product_id: quantity
    status: OrderStatus = OrderStatus.PENDING
    total_amount: float = 0.0

    def calculate_total(self, product_prices: Dict[str, float]):
        """Calculate total order amount"""
        self.total_amount = sum(
            quantity * product_prices[prod_id]
            for prod_id, quantity in self.products.items()
        )
        return self.total_amount

    def update_status(self, status: OrderStatus):
        """Update order status"""
        self.status = status 