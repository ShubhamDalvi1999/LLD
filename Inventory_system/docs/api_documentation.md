# API Documentation

## Core Classes and Methods

### 1. InventorySystem Class

#### Methods

##### `add_product(product: Product) -> bool`
- **Description**: Adds a new product to the system
- **Parameters**: 
  - `product`: Product object containing product details
- **Returns**: Boolean indicating success/failure
- **Thread Safety**: Thread-safe
- **Example**:
```python
product = Product(
    product_id="123",
    name="Laptop",
    description="High-performance laptop",
    price=999.99,
    weight=2.5,
    dimensions={'length': 35, 'width': 25, 'height': 2}
)
success = system.add_product(product)
```

##### `update_product(product: Product) -> bool`
- **Description**: Updates existing product details
- **Parameters**: 
  - `product`: Product object with updated details
- **Returns**: Boolean indicating success/failure
- **Thread Safety**: Thread-safe

##### `add_unit(unit: Unit) -> bool`
- **Description**: Adds a new unit to inventory with location assignment
- **Parameters**: 
  - `unit`: Unit object to be added
- **Returns**: Boolean indicating success/failure
- **Thread Safety**: Thread-safe using location locks

##### `remove_unit(unit_id: str) -> bool`
- **Description**: Removes a unit from inventory
- **Parameters**: 
  - `unit_id`: Unique identifier of the unit
- **Returns**: Boolean indicating success/failure
- **Thread Safety**: Thread-safe using location locks

##### `place_order(order: Order) -> bool`
- **Description**: Places a new order in the system
- **Parameters**: 
  - `order`: Order object containing order details
- **Returns**: Boolean indicating success/failure
- **Thread Safety**: Thread-safe

##### `process_order(order_id: str) -> bool`
- **Description**: Processes an existing order
- **Parameters**: 
  - `order_id`: Unique identifier of the order
- **Returns**: Boolean indicating success/failure
- **Thread Safety**: Thread-safe

### 2. Product Class

#### Attributes
- `product_id: str`: Unique identifier
- `name: str`: Product name
- `description: str`: Product description
- `price: float`: Product price
- `weight: float`: Product weight
- `dimensions: Dict[str, float]`: Product dimensions

#### Methods
- `update_details(**kwargs)`: Update product details
- `get_details() -> Dict`: Get product details as dictionary

### 3. Unit Class

#### Attributes
- `unit_id: str`: Unique identifier
- `product_id: str`: Associated product ID
- `location_id: str`: Current location ID
- `status: UnitStatus`: Current unit status

#### Methods
- `update_location(location_id: str)`: Update unit location
- `update_status(status: UnitStatus)`: Update unit status

### 4. Location Class

#### Attributes
- `location_id: str`: Unique identifier
- `type: str`: Location type (small/medium/large)
- `dimensions: Dict[str, float]`: Location dimensions
- `is_occupied: bool`: Occupancy status

#### Methods
- `occupy() -> bool`: Mark location as occupied
- `vacate() -> bool`: Mark location as available
- `is_available() -> bool`: Check availability

### 5. Order Class

#### Attributes
- `order_id: str`: Unique identifier
- `customer_id: str`: Customer identifier
- `products: Dict[str, int]`: Product IDs and quantities
- `status: OrderStatus`: Current order status
- `total_amount: float`: Total order amount

#### Methods
- `calculate_total(product_prices: Dict[str, float])`: Calculate order total
- `update_status(status: OrderStatus)`: Update order status 