from sqlalchemy import Column, String, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship, validates
from enum import Enum
from .database import Base

class UnitStatus(str, Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"

class Unit(Base):
    __tablename__ = "units"

    unit_id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey("products.product_id"), nullable=False)
    location_id = Column(String, ForeignKey("locations.location_id"))
    status = Column(SQLEnum(UnitStatus), nullable=False, default=UnitStatus.AVAILABLE)

    # Relationships
    product = relationship("Product", lazy="joined")
    location = relationship("Location", lazy="joined")

    @validates('status')
    def validate_status_transition(self, key, status):
        """Validate status transitions"""
        if hasattr(self, 'status'):
            valid_transitions = {
                UnitStatus.AVAILABLE: {UnitStatus.RESERVED},
                UnitStatus.RESERVED: {UnitStatus.IN_TRANSIT, UnitStatus.AVAILABLE},
                UnitStatus.IN_TRANSIT: {UnitStatus.DELIVERED},
                UnitStatus.DELIVERED: {UnitStatus.AVAILABLE}
            }
            if status not in valid_transitions[self.status]:
                raise ValueError(f"Invalid status transition from {self.status} to {status}")
        return status

    def update_location(self, location_id: str):
        """Update unit location"""
        if self.status != UnitStatus.AVAILABLE:
            raise ValueError("Cannot move unit that is not available")
        self.location_id = location_id

    def update_status(self, status: UnitStatus):
        """Update unit status with validation"""
        self.status = status  # This will trigger validate_status_transition

    def to_dict(self):
        """Convert unit to dictionary"""
        return {
            'unit_id': self.unit_id,
            'product_id': self.product_id,
            'location_id': self.location_id,
            'status': self.status.value
        } 