from dataclasses import dataclass
from enum import Enum

class UnitStatus(Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"

@dataclass
class Unit:
    unit_id: str
    product_id: str
    location_id: str = None
    status: UnitStatus = UnitStatus.AVAILABLE

    def update_location(self, location_id: str):
        """Update unit location"""
        self.location_id = location_id

    def update_status(self, status: UnitStatus):
        """Update unit status"""
        self.status = status 