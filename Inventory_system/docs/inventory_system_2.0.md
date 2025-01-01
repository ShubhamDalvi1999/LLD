# Inventory Management System 2.0

## Overview of Improvements

The Inventory Management System has been refactored to address several key issues and implement modern software design patterns. Here are the major improvements:

### 1. Decentralized Architecture
- Split monolithic `InventorySystem` into specialized managers:
  - `ProductManager`: Handles product lifecycle
  - `LocationManager`: Manages warehouse spaces
  - `OrderManager`: Processes orders
  - `UnitManager`: Tracks individual units

### 2. Persistence Layer
- Implemented SQLAlchemy ORM for database operations
- Proper model relationships and validations
- Transaction management and rollback support
- Session handling and connection pooling

### 3. Concurrency Handling
- Database-level transaction management
- Proper exception handling with rollbacks
- State transition validation
- Thread-safe operations

### 4. Enhanced Validation
- Field-level validation using SQLAlchemy validators
- Business rule validation
- State transition validation
- Input data validation

### 5. Event-Driven Architecture
- Event listeners for status changes
- Proper event handling for state transitions
- Asynchronous event processing capability

## System Components

### 1. Database Models

#### Product Model
```python
class Product(Base):
    __tablename__ = "products"
    product_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    dimensions = Column(JSON, nullable=False)
```

#### Unit Model
```python
class Unit(Base):
    __tablename__ = "units"
    unit_id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey("products.product_id"))
    location_id = Column(String, ForeignKey("locations.location_id"))
    status = Column(SQLEnum(UnitStatus))
```

#### Location Model
```python
class Location(Base):
    __tablename__ = "locations"
    location_id = Column(String, primary_key=True)
    type = Column(SQLEnum(LocationType))
    dimensions = Column(JSON)
    is_occupied = Column(Boolean)
```

#### Order Model
```python
class Order(Base):
    __tablename__ = "orders"
    order_id = Column(String, primary_key=True)
    customer_id = Column(String)
    products = Column(JSON)  # {product_id: quantity}
    status = Column(SQLEnum(OrderStatus))
    total_amount = Column(Float)
```

### 2. Manager Classes

#### ProductManager
- Product CRUD operations
- Product validation
- Product search functionality

```python
class ProductManager:
    def create_product(self, product: Product) -> Product
    def update_product(self, product: Product) -> Product
    def delete_product(self, product_id: str) -> bool
    def list_products(self) -> List[Product]
    def search_products(self, **filters) -> List[Product]
```

#### LocationManager
- Location management
- Space allocation strategies
- Occupancy tracking

```python
class LocationManager:
    def create_location(self, location: Location) -> Location
    def find_suitable_location(self, product: Product) -> Optional[Location]
    def update_location_status(self, location_id: str, is_occupied: bool) -> bool
    def list_available_locations(self) -> List[Location]
```

#### OrderManager
- Order processing
- Status management
- Inventory allocation

```python
class OrderManager:
    def create_order(self, order: Order) -> Order
    def process_order(self, order_id: str) -> bool
    def cancel_order(self, order_id: str) -> bool
    def list_orders(self, status: Optional[OrderStatus] = None) -> List[Order]
```

#### UnitManager
- Unit tracking
- Location assignment
- Status management

```python
class UnitManager:
    def create_unit(self, unit: Unit, location: Optional[Location] = None) -> Unit
    def update_unit_location(self, unit_id: str, location_id: str) -> bool
    def update_unit_status(self, unit_id: str, status: UnitStatus) -> bool
    def remove_unit(self, unit_id: str) -> bool
```

### 3. Design Patterns

#### Strategy Pattern (Location Finding)
```python
class LocationStrategy(ABC):
    @abstractmethod
    def find_location(self, product: Product, locations: List[Location]) -> Optional[Location]:
        pass

class NearestEntranceStrategy(LocationStrategy):
    def find_location(self, product: Product, locations: List[Location]) -> Optional[Location]:
        # Implementation for finding nearest location

class OptimalSpaceStrategy(LocationStrategy):
    def find_location(self, product: Product, locations: List[Location]) -> Optional[Location]:
        # Implementation for finding optimal space
```

#### Event Listener Pattern (Order Status)
```python
@event.listens_for(Order.status, 'set')
def order_status_change(target, value, oldvalue, initiator):
    if value == OrderStatus.PROCESSING:
        # Reserve units
    elif value == OrderStatus.SHIPPED:
        # Update unit locations
    elif value == OrderStatus.DELIVERED:
        # Update inventory
```

### 4. Error Handling

```python
try:
    # Operation logic
    self.db.commit()
    return True
except Exception as e:
    self.db.rollback()
    logger.error(f"Error: {str(e)}")
    return False
```

## Usage Example

```python
# Initialize system with database session
db = SessionLocal()
system = InventorySystem(db)

# Set location finding strategy
system.set_location_strategy(OptimalSpaceStrategy())

# Create product
product = Product(
    product_id=str(uuid.uuid4()),
    name="Laptop",
    description="High-performance laptop",
    price=999.99,
    weight=2.5,
    dimensions={'length': 35, 'width': 25, 'height': 2}
)
system.add_product(product)

# Create unit
unit = Unit(
    unit_id=str(uuid.uuid4()),
    product_id=product.product_id
)
system.add_unit(unit)

# Create order
order = Order(
    order_id=str(uuid.uuid4()),
    customer_id=str(uuid.uuid4()),
    products={product.product_id: 1}
)
system.place_order(order)
```

## Future Improvements

1. **Caching Layer**
   - Implement Redis for caching frequently accessed data
   - Cache invalidation strategies
   - Distributed caching support

2. **API Layer**
   - RESTful API endpoints
   - GraphQL support
   - API versioning

3. **Authentication/Authorization**
   - Role-based access control
   - JWT authentication
   - Permission management

4. **Monitoring and Logging**
   - Prometheus metrics
   - ELK stack integration
   - Performance monitoring

5. **Scalability**
   - Microservices architecture
   - Message queues for async operations
   - Load balancing strategies 