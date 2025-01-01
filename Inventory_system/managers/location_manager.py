from sqlalchemy.orm import Session
from ..models.location import Location, LocationType
from ..models.product import Product
from typing import List, Optional, Protocol, Dict
from abc import ABC, abstractmethod

class LocationStrategy(ABC):
    @abstractmethod
    def find_location(self, product: Product, locations: List[Location]) -> Optional[Location]:
        pass

class NearestEntranceStrategy(LocationStrategy):
    def find_location(self, product: Product, locations: List[Location]) -> Optional[Location]:
        """Find location nearest to entrance"""
        # In a real system, locations would have coordinates
        # For now, just return first available matching location
        for location in locations:
            if (location.is_available() and 
                all(product.dimensions[k] <= location.dimensions[k] 
                    for k in ['length', 'width', 'height'])):
                return location
        return None

class OptimalSpaceStrategy(LocationStrategy):
    def find_location(self, product: Product, locations: List[Location]) -> Optional[Location]:
        """Find location with least wasted space"""
        best_location = None
        min_waste = float('inf')
        
        for location in locations:
            if not location.is_available():
                continue
                
            if all(product.dimensions[k] <= location.dimensions[k] 
                  for k in ['length', 'width', 'height']):
                waste = sum(location.dimensions[k] - product.dimensions[k] 
                          for k in ['length', 'width', 'height'])
                if waste < min_waste:
                    min_waste = waste
                    best_location = location
                    
        return best_location

class LocationManager:
    def __init__(self, db: Session):
        self.db = db
        self.strategy: LocationStrategy = NearestEntranceStrategy()

    def set_strategy(self, strategy: LocationStrategy):
        """Set location finding strategy"""
        self.strategy = strategy

    def create_location(self, location: Location) -> Location:
        """Create a new location"""
        self.db.add(location)
        self.db.commit()
        self.db.refresh(location)
        return location

    def get_location(self, location_id: str) -> Optional[Location]:
        """Get location by ID"""
        return self.db.query(Location).filter(Location.location_id == location_id).first()

    def find_suitable_location(self, product: Product) -> Optional[Location]:
        """Find suitable location using current strategy"""
        available_locations = (
            self.db.query(Location)
            .filter(Location.is_occupied == False)
            .all()
        )
        return self.strategy.find_location(product, available_locations)

    def update_location_status(self, location_id: str, is_occupied: bool) -> bool:
        """Update location occupancy status"""
        location = self.get_location(location_id)
        if not location:
            return False
            
        if is_occupied:
            success = location.occupy()
        else:
            success = location.vacate()
            
        if success:
            self.db.commit()
        return success

    def list_available_locations(self) -> List[Location]:
        """List all available locations"""
        return self.db.query(Location).filter(Location.is_occupied == False).all()

    def get_locations_by_type(self, location_type: LocationType) -> List[Location]:
        """Get locations by type"""
        return self.db.query(Location).filter(Location.type == location_type).all() 