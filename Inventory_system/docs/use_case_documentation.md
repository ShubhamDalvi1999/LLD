# Use Case Documentation

## 1. Product Management Use Cases

### 1.1 Add New Product
- **Actor**: Administrator
- **Description**: Add a new product to the inventory system
- **Preconditions**: 
  - Administrator is authenticated
  - Product details are valid
- **Main Flow**:
  1. Administrator enters product details
  2. System validates input
  3. System creates product record
  4. System confirms creation
- **Alternative Flows**:
  - Product already exists
  - Invalid product details
- **Postconditions**: 
  - New product added to system
  - Product available for unit creation

### 1.2 Update Product
- **Actor**: Administrator
- **Description**: Modify existing product details
- **Preconditions**: 
  - Product exists in system
  - Administrator is authenticated
- **Main Flow**:
  1. Administrator selects product
  2. System displays current details
  3. Administrator modifies details
  4. System validates changes
  5. System updates product
- **Alternative Flows**:
  - Product not found
  - Invalid updates
- **Postconditions**: 
  - Product details updated
  - Existing units unaffected

## 2. Unit Management Use Cases

### 2.1 Add Unit
- **Actor**: Warehouse Manager
- **Description**: Add physical unit to inventory
- **Preconditions**: 
  - Product exists
  - Location available
- **Main Flow**:
  1. Manager creates unit for product
  2. System finds suitable location
  3. System assigns location
  4. System confirms addition
- **Alternative Flows**:
  - No suitable location
  - Product not found
- **Postconditions**: 
  - Unit added to inventory
  - Location marked occupied

### 2.2 Remove Unit
- **Actor**: Warehouse Manager
- **Description**: Remove unit from inventory
- **Preconditions**: 
  - Unit exists in system
  - Unit not in active order
- **Main Flow**:
  1. Manager selects unit
  2. System validates removal
  3. System updates inventory
  4. Location freed
- **Alternative Flows**:
  - Unit in active order
  - Unit not found
- **Postconditions**: 
  - Unit removed
  - Location available

## 3. Order Processing Use Cases

### 3.1 Place Order
- **Actor**: Customer
- **Description**: Create new order
- **Preconditions**: 
  - Products available
  - Customer authenticated
- **Main Flow**:
  1. Customer selects products
  2. System checks availability
  3. System calculates total
  4. Customer confirms order
  5. System creates order
- **Alternative Flows**:
  - Insufficient inventory
  - Invalid product selection
- **Postconditions**: 
  - Order created
  - Units reserved

### 3.2 Process Order
- **Actor**: System
- **Description**: Handle order fulfillment
- **Preconditions**: 
  - Valid order exists
  - Units available
- **Main Flow**:
  1. System validates order
  2. System allocates units
  3. System updates inventory
  4. System updates order status
- **Alternative Flows**:
  - Order validation fails
  - Unit allocation fails
- **Postconditions**: 
  - Order processed
  - Units status updated

## 4. Reporting Use Cases

### 4.1 Generate Inventory Report
- **Actor**: Administrator
- **Description**: Create system report
- **Preconditions**: 
  - Administrator authenticated
- **Main Flow**:
  1. Administrator requests report
  2. System collects data
  3. System generates report
  4. System presents report
- **Alternative Flows**:
  - Data collection error
- **Postconditions**: 
  - Report generated
  - Statistics updated 