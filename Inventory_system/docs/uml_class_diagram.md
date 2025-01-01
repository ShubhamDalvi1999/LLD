# UML Class Diagram Documentation

## Class Diagram

```mermaid
classDiagram
    class InventorySystem {
        -products: Dict[str, Product]
        -units: Dict[str, Unit]
        -locations: Dict[str, Location]
        -orders: Dict[str, Order]
        -locks: Dict[str, Lock]
        +add_product(product: Product) bool
        +update_product(product: Product) bool
        +add_unit(unit: Unit) bool
        +remove_unit(unit_id: str) bool
        +place_order(order: Order) bool
        +process_order(order_id: str) bool
        +generate_report() Dict
        -find_suitable_location(unit: Unit) Location
        -can_fit(product_dim: Dict, location_dim: Dict) bool
    }

    class Product {
        +product_id: str
        +name: str
        +description: str
        +price: float
        +weight: float
        +dimensions: Dict[str, float]
        +update_details(**kwargs)
        +get_details() Dict
    }

    class Unit {
        +unit_id: str
        +product_id: str
        +location_id: str
        +status: UnitStatus
        +update_location(location_id: str)
        +update_status(status: UnitStatus)
    }

    class Location {
        +location_id: str
        +type: str
        +dimensions: Dict[str, float]
        +is_occupied: bool
        +occupy() bool
        +vacate() bool
        +is_available() bool
    }

    class Order {
        +order_id: str
        +customer_id: str
        +products: Dict[str, int]
        +status: OrderStatus
        +total_amount: float
        +calculate_total(product_prices: Dict)
        +update_status(status: OrderStatus)
    }

    class UnitStatus {
        <<enumeration>>
        AVAILABLE
        RESERVED
        IN_TRANSIT
        DELIVERED
    }

    class OrderStatus {
        <<enumeration>>
        PENDING
        PROCESSING
        SHIPPED
        DELIVERED
        CANCELLED
    }

    InventorySystem "1" -- "*" Product
    InventorySystem "1" -- "*" Unit
    InventorySystem "1" -- "*" Location
    InventorySystem "1" -- "*" Order
    Product "1" -- "*" Unit
    Unit "1" -- "1" Location
    Unit -- UnitStatus
    Order -- OrderStatus
```

## Relationships

### 1. InventorySystem Relationships
- Has many Products (1:*)
- Has many Units (1:*)
- Has many Locations (1:*)
- Has many Orders (1:*)
- Manages all interactions between classes

### 2. Product Relationships
- One Product can have many Units (1:*)
- Products are referenced by Orders

### 3. Unit Relationships
- Belongs to one Product (1:1)
- Occupies one Location (1:1)
- Has one UnitStatus

### 4. Location Relationships
- Can contain one Unit (1:1)
- Managed by InventorySystem

### 5. Order Relationships
- Contains multiple Products
- Has one OrderStatus
- Managed by InventorySystem

## Class Responsibilities

### InventorySystem
- Central system management
- Coordination between components
- Thread safety enforcement
- Business logic implementation

### Product
- Product information storage
- Product detail management
- Product validation

### Unit
- Physical item representation
- Location tracking
- Status management

### Location
- Storage space representation
- Occupancy management
- Space validation

### Order
- Order information storage
- Order processing logic
- Status tracking

## Enumerations

### UnitStatus
- Defines possible unit states
- Ensures valid state transitions
- Used for inventory tracking

### OrderStatus
- Defines possible order states
- Ensures valid order progression
- Used for order tracking 