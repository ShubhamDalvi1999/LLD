from inventory_system import InventorySystem
from models.product import Product
from models.unit import Unit
from models.location import Location
from models.order import Order
import uuid

def main():
    # Initialize the system
    system = InventorySystem()

    # Add some locations
    location = Location(
        location_id=str(uuid.uuid4()),
        type="medium",
        dimensions={'length': 100, 'width': 100, 'height': 100}
    )
    system.locations[location.location_id] = location

    # Add a product
    product = Product(
        product_id=str(uuid.uuid4()),
        name="Laptop",
        description="High-performance laptop",
        price=999.99,
        weight=2.5,
        dimensions={'length': 35, 'width': 25, 'height': 2}
    )
    system.add_product(product)

    # Add a unit
    unit = Unit(
        unit_id=str(uuid.uuid4()),
        product_id=product.product_id
    )
    system.add_unit(unit)

    # Create an order
    order = Order(
        order_id=str(uuid.uuid4()),
        customer_id=str(uuid.uuid4()),
        products={product.product_id: 1}
    )
    
    # Place and process order
    if system.place_order(order):
        system.process_order(order.order_id)

    # Generate report
    report = system.generate_report()
    print("Inventory Report:", report)

if __name__ == "__main__":
    main() 