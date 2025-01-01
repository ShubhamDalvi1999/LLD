from typing import Dict, List, Optional
import threading
from .models.product import Product
from .models.unit import Unit, UnitStatus
from .models.location import Location
from .models.order import Order, OrderStatus

class InventorySystem:
    def __init__(self):
        self.products: Dict[str, Product] = {}
        self.units: Dict[str, Unit] = {}
        self.locations: Dict[str, Location] = {}
        self.orders: Dict[str, Order] = {}
        self.locks: Dict[str, threading.Lock] = {}

    def add_product(self, product: Product) -> bool:
        """Add a new product to the system"""
        if product.product_id not in self.products:
            self.products[product.product_id] = product
            return True
        return False

    def update_product(self, product: Product) -> bool:
        """Update existing product details"""
        if product.product_id in self.products:
            self.products[product.product_id] = product
            return True
        return False

    def add_unit(self, unit: Unit) -> bool:
        """Add a new unit to inventory"""
        if unit.product_id not in self.products:
            return False

        location = self._find_suitable_location(unit)
        if not location:
            return False

        # Get or create lock for the location
        lock = self.locks.setdefault(location.location_id, threading.Lock())

        with lock:
            if location.occupy():
                unit.update_location(location.location_id)
                self.units[unit.unit_id] = unit
                return True
        return False

    def remove_unit(self, unit_id: str) -> bool:
        """Remove a unit from inventory"""
        if unit_id not in self.units:
            return False

        unit = self.units[unit_id]
        if unit.location_id:
            location = self.locations[unit.location_id]
            lock = self.locks.get(location.location_id)
            
            if lock:
                with lock:
                    location.vacate()
                    del self.units[unit_id]
                    return True
        return False

    def place_order(self, order: Order) -> bool:
        """Place a new order"""
        # Verify products availability
        for product_id, quantity in order.products.items():
            available_units = sum(
                1 for unit in self.units.values()
                if unit.product_id == product_id and unit.status == UnitStatus.AVAILABLE
            )
            if available_units < quantity:
                return False

        # Calculate total amount
        order.calculate_total({p.product_id: p.price for p in self.products.values()})
        self.orders[order.order_id] = order
        return True

    def process_order(self, order_id: str) -> bool:
        """Process an existing order"""
        if order_id not in self.orders:
            return False

        order = self.orders[order_id]
        if order.status != OrderStatus.PENDING:
            return False

        order.update_status(OrderStatus.PROCESSING)

        # Allocate units to order
        for product_id, quantity in order.products.items():
            allocated_units = 0
            for unit in self.units.values():
                if (unit.product_id == product_id and 
                    unit.status == UnitStatus.AVAILABLE and 
                    allocated_units < quantity):
                    unit.update_status(UnitStatus.RESERVED)
                    allocated_units += 1

        order.update_status(OrderStatus.SHIPPED)
        return True

    def generate_report(self) -> Dict:
        """Generate inventory report"""
        return {
            'total_products': len(self.products),
            'total_units': len(self.units),
            'available_locations': sum(1 for loc in self.locations.values() if not loc.is_occupied),
            'pending_orders': sum(1 for order in self.orders.values() if order.status == OrderStatus.PENDING)
        }

    def _find_suitable_location(self, unit: Unit) -> Optional[Location]:
        """Find suitable location for a unit"""
        product = self.products[unit.product_id]
        for location in self.locations.values():
            if (not location.is_occupied and 
                self._can_fit(product.dimensions, location.dimensions)):
                return location
        return None

    def _can_fit(self, product_dim: Dict[str, float], location_dim: Dict[str, float]) -> bool:
        """Check if product can fit in location"""
        return all(
            product_dim[dim] <= location_dim[dim]
            for dim in ['length', 'width', 'height']
        ) 