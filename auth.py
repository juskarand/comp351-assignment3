import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from jose import jwt, JWTError
from fastapi import Depends, Header, Cookie, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
import crud

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY missing (set it in .env).")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None

def get_token(
    authorization: Optional[str] = Header(default=None),
    access_token: Optional[str] = Cookie(default=None),
) -> Optional[str]:
    # Support Bearer (optional) + cookie (chosen strategy)
    if authorization and authorization.startswith("Bearer "):
        return authorization.split(" ", 1)[1].strip()
    return access_token

def get_current_user(
    token: Optional[str] = Depends(get_token),
    db: Session = Depends(get_db),
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User inactive")

    return user

def require_admin(current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin required")
    return current_user
