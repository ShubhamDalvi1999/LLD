from dataclasses import dataclass
from typing import Dict

@dataclass
class Location:
    location_id: str
    type: str  # 'small', 'medium', 'large'
    dimensions: Dict[str, float]
    is_occupied: bool = False

    def occupy(self):
        """Mark location as occupied"""
        if not self.is_occupied:
            self.is_occupied = True
            return True
        return False

    def vacate(self):
        """Mark location as available"""
        if self.is_occupied:
            self.is_occupied = False
            return True
        return False

    def is_available(self) -> bool:
        """Check if location is available"""
        return not self.is_occupied 