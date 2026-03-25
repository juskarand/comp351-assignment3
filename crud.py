from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import User, InventoryItem

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, username: str, email: str, hashed_password: str):
    user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def list_items(db: Session, q=None, skip=0, limit=50):
    query = db.query(InventoryItem)
    if q:
        like = f"%{q.strip()}%"
        query = query.filter(
            or_(
                InventoryItem.sku.ilike(like),
                InventoryItem.name.ilike(like),
                InventoryItem.location.ilike(like),
            )
        )
    return query.offset(skip).limit(limit).all()
