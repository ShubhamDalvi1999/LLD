from sqlalchemy.orm import Session
from ..models.unit import Unit, UnitStatus
from ..models.product import Product
from ..models.location import Location
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class UnitManager:
    def __init__(self, db: Session):
        self.db = db

    def create_unit(self, unit: Unit, location: Optional[Location] = None) -> Unit:
        """Create a new unit"""
        # Verify product exists
        product = self.db.query(Product).filter(Product.product_id == unit.product_id).first()
        if not product:
            raise ValueError("Product not found")

        if location:
            if not location.is_available():
                raise ValueError("Location is not available")
            unit.location_id = location.location_id
            location.occupy()

        self.db.add(unit)
        self.db.commit()
        self.db.refresh(unit)
        return unit

    def get_unit(self, unit_id: str) -> Optional[Unit]:
        """Get unit by ID"""
        return self.db.query(Unit).filter(Unit.unit_id == unit_id).first()

    def update_unit_location(self, unit_id: str, location_id: str) -> bool:
        """Update unit location"""
        unit = self.get_unit(unit_id)
        if not unit:
            return False

        try:
            # Release old location if exists
            if unit.location_id:
                old_location = (
                    self.db.query(Location)
                    .filter(Location.location_id == unit.location_id)
                    .first()
                )
                if old_location:
                    old_location.vacate()

            # Occupy new location
            new_location = (
                self.db.query(Location)
                .filter(Location.location_id == location_id)
                .first()
            )
            if not new_location or not new_location.is_available():
                raise ValueError("New location not available")

            unit.location_id = location_id
            new_location.occupy()
            
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating unit location: {str(e)}")
            return False

    def update_unit_status(self, unit_id: str, status: UnitStatus) -> bool:
        """Update unit status"""
        unit = self.get_unit(unit_id)
        if not unit:
            return False

        try:
            unit.status = status
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating unit status: {str(e)}")
            return False

    def list_units(self, 
                  product_id: Optional[str] = None, 
                  status: Optional[UnitStatus] = None) -> List[Unit]:
        """List units with optional filters"""
        query = self.db.query(Unit)
        
        if product_id:
            query = query.filter(Unit.product_id == product_id)
        if status:
            query = query.filter(Unit.status == status)
            
        return query.all()

    def get_available_units(self, product_id: str) -> List[Unit]:
        """Get available units for a product"""
        return (
            self.db.query(Unit)
            .filter(Unit.product_id == product_id)
            .filter(Unit.status == UnitStatus.AVAILABLE)
            .all()
        )

    def remove_unit(self, unit_id: str) -> bool:
        """Remove a unit from inventory"""
        unit = self.get_unit(unit_id)
        if not unit:
            return False

        try:
            # Release location if occupied
            if unit.location_id:
                location = (
                    self.db.query(Location)
                    .filter(Location.location_id == unit.location_id)
                    .first()
                )
                if location:
                    location.vacate()

            self.db.delete(unit)
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error removing unit: {str(e)}")
            return False 