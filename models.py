from sqlalchemy import Column, Integer, String, Float, Boolean, Index
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(200), unique=True, nullable=False, index=True)
    hashed_password = Column(String(200), nullable=False)  # never plaintext
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    quantity = Column(Integer, nullable=False, default=0, index=True)
    unit_price = Column(Float, nullable=False, default=0.0)
    reorder_level = Column(Integer, nullable=False, default=0)
    location = Column(String(120), nullable=True, index=True)
    is_active = Column(Boolean, default=True)

Index("ix_inventory_name_sku", InventoryItem.name, InventoryItem.sku)
