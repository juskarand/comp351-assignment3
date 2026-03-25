from dotenv import load_dotenv
load_dotenv()

import os
from typing import Optional, List

from fastapi import FastAPI, Depends, HTTPException, Response, Request, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import User, InventoryItem
from schemas import RegisterRequest, LoginRequest, UserResponse, ItemResponse
import crud
from auth import hash_password, verify_password, create_access_token, get_current_user, require_admin

app = FastAPI(title="Assignment 3 - Security Integration")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

Base.metadata.create_all(bind=engine)

COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"
MAX_AGE = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")) * 60

@app.get("/")
def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/api/register", response_model=UserResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, payload.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    if crud.get_user_by_email(db, payload.email.lower()):
        raise HTTPException(status_code=400, detail="Email already exists")

    user = crud.create_user(
        db,
        username=payload.username.strip(),
        email=payload.email.lower().strip(),
        hashed_password=hash_password(payload.password),
    )
    return user

@app.post("/api/login")
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, payload.username)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=COOKIE_SECURE,   # False acceptable on localhost
        samesite="lax",
        max_age=MAX_AGE,
    )
    return {"message": "Login successful"}

@app.post("/api/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logged out"}

@app.get("/api/me", response_model=UserResponse)
def me(current_user=Depends(get_current_user)):
    return current_user

@app.get("/api/items", response_model=List[ItemResponse])
def items(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    q: Optional[str] = Query(default=None),
    skip: int = 0,
    limit: int = 50,
):
    return crud.list_items(db, q=q, skip=skip, limit=limit)

@app.get("/api/admin", response_model=UserResponse)
def admin_only(admin_user=Depends(require_admin)):
    return admin_user
