from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from .models.product import Product
from .models.unit import Unit, UnitStatus
from .models.location import Location, LocationType
from .models.order import Order, OrderStatus
from .managers.product_manager import ProductManager
from .managers.location_manager import LocationManager, LocationStrategy
from .managers.order_manager import OrderManager
from .managers.unit_manager import UnitManager
import logging

logger = logging.getLogger(__name__)

class InventorySystem:
    def __init__(self, db: Session):
        """Initialize managers with database session"""
        self.db = db
        self.product_manager = ProductManager(db)
        self.location_manager = LocationManager(db)
        self.order_manager = OrderManager(db)
        self.unit_manager = UnitManager(db)

    def set_location_strategy(self, strategy: LocationStrategy):
        """Set location finding strategy"""
        self.location_manager.set_strategy(strategy)

    # Product Operations
    def add_product(self, product: Product) -> bool:
        """Add a new product"""
        try:
            self.product_manager.create_product(product)
            return True
        except Exception as e:
            logger.error(f"Error adding product: {str(e)}")
            return False

    def update_product(self, product: Product) -> bool:
        """Update existing product"""
        try:
            self.product_manager.update_product(product)
            return True
        except Exception as e:
            logger.error(f"Error updating product: {str(e)}")
            return False

    # Unit Operations
    def add_unit(self, unit: Unit) -> bool:
        """Add a new unit to inventory"""
        try:
            # Find suitable location
            location = self.location_manager.find_suitable_location(
                self.product_manager.get_product(unit.product_id)
            )
            if not location:
                return False

            self.unit_manager.create_unit(unit, location)
            return True
        except Exception as e:
            logger.error(f"Error adding unit: {str(e)}")
            return False

    def remove_unit(self, unit_id: str) -> bool:
        """Remove a unit from inventory"""
        return self.unit_manager.remove_unit(unit_id)

    # Order Operations
    def place_order(self, order: Order) -> bool:
        """Place a new order"""
        try:
            self.order_manager.create_order(order)
            return True
        except Exception as e:
            logger.error(f"Error placing order: {str(e)}")
            return False

    def process_order(self, order_id: str) -> bool:
        """Process an existing order"""
        return self.order_manager.process_order(order_id)

    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order"""
        return self.order_manager.cancel_order(order_id)

    # Location Operations
    def add_location(self, location: Location) -> bool:
        """Add a new location"""
        try:
            self.location_manager.create_location(location)
            return True
        except Exception as e:
            logger.error(f"Error adding location: {str(e)}")
            return False

    # Reporting
    def generate_report(self) -> Dict:
        """Generate inventory report"""
        try:
            total_products = len(self.product_manager.list_products())
            total_units = len(self.unit_manager.list_units())
            available_locations = len(self.location_manager.list_available_locations())
            pending_orders = len(self.order_manager.list_orders(OrderStatus.PENDING))

            return {
                'total_products': total_products,
                'total_units': total_units,
                'available_locations': available_locations,
                'pending_orders': pending_orders
            }
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return {} 