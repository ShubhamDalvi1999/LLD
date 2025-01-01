from sqlalchemy.orm import Session
from ..models.product import Product
from typing import List, Optional

class ProductManager:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product: Product) -> Product:
        """Create a new product"""
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_product(self, product_id: str) -> Optional[Product]:
        """Get product by ID"""
        return self.db.query(Product).filter(Product.product_id == product_id).first()

    def update_product(self, product: Product) -> Product:
        """Update existing product"""
        existing = self.get_product(product.product_id)
        if not existing:
            raise ValueError("Product not found")
        
        for key, value in product.to_dict().items():
            setattr(existing, key, value)
        
        self.db.commit()
        self.db.refresh(existing)
        return existing

    def delete_product(self, product_id: str) -> bool:
        """Delete product by ID"""
        product = self.get_product(product_id)
        if not product:
            return False
        
        self.db.delete(product)
        self.db.commit()
        return True

    def list_products(self) -> List[Product]:
        """List all products"""
        return self.db.query(Product).all()

    def search_products(self, **filters) -> List[Product]:
        """Search products with filters"""
        query = self.db.query(Product)
        
        for key, value in filters.items():
            if hasattr(Product, key):
                query = query.filter(getattr(Product, key) == value)
        
        return query.all() 