from sqlalchemy import Column, String, Boolean, JSON, Enum as SQLEnum
from sqlalchemy.orm import validates
from enum import Enum
from .database import Base

class LocationType(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

class Location(Base):
    __tablename__ = "locations"

    location_id = Column(String, primary_key=True)
    type = Column(SQLEnum(LocationType), nullable=False)
    dimensions = Column(JSON, nullable=False)
    is_occupied = Column(Boolean, default=False)

    @validates('dimensions')
    def validate_dimensions(self, key, dimensions):
        """Validate dimensions dictionary"""
        required_keys = {'length', 'width', 'height'}
        if not all(k in dimensions for k in required_keys):
            raise ValueError("Dimensions must include length, width, and height")
        if not all(isinstance(dimensions[k], (int, float)) and dimensions[k] > 0 for k in required_keys):
            raise ValueError("All dimensions must be positive numbers")
        return dimensions

    def occupy(self) -> bool:
        """Mark location as occupied"""
        if not self.is_occupied:
            self.is_occupied = True
            return True
        return False

    def vacate(self) -> bool:
        """Mark location as available"""
        if self.is_occupied:
            self.is_occupied = False
            return True
        return False

    def is_available(self) -> bool:
        """Check if location is available"""
        return not self.is_occupied

    def to_dict(self):
        """Convert location to dictionary"""
        return {
            'location_id': self.location_id,
            'type': self.type.value,
            'dimensions': self.dimensions,
            'is_occupied': self.is_occupied
        } 