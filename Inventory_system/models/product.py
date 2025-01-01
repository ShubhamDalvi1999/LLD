from sqlalchemy import Column, String, Float, JSON
from sqlalchemy.orm import validates
from .database import Base

class Product(Base):
    __tablename__ = "products"

    product_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    dimensions = Column(JSON, nullable=False)  # {'length': x, 'width': y, 'height': z}

    @validates('price', 'weight')
    def validate_positive_number(self, key, value):
        """Validate price and weight are positive"""
        if value <= 0:
            raise ValueError(f"{key} must be positive")
        return value

    @validates('dimensions')
    def validate_dimensions(self, key, dimensions):
        """Validate dimensions dictionary"""
        required_keys = {'length', 'width', 'height'}
        if not all(k in dimensions for k in required_keys):
            raise ValueError("Dimensions must include length, width, and height")
        if not all(isinstance(dimensions[k], (int, float)) and dimensions[k] > 0 for k in required_keys):
            raise ValueError("All dimensions must be positive numbers")
        return dimensions

    def to_dict(self):
        """Convert product to dictionary"""
        return {
            'product_id': self.product_id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'weight': self.weight,
            'dimensions': self.dimensions
        } 