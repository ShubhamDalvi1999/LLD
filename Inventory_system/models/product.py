from dataclasses import dataclass
from typing import Dict

@dataclass
class Product:
    product_id: str
    name: str
    description: str
    price: float
    weight: float
    dimensions: Dict[str, float]  # {'length': x, 'width': y, 'height': z}

    def update_details(self, **kwargs):
        """Update product details"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def get_details(self) -> Dict:
        """Return product details as dictionary"""
        return {
            'product_id': self.product_id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'weight': self.weight,
            'dimensions': self.dimensions
        } 