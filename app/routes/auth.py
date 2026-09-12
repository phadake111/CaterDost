from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import User

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication & Profile"])

class SignUpSchema(BaseModel):
    business_name: str
    phone: str
    pin: str

class LoginSchema(BaseModel):
    phone: str
    pin: str

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(data: SignUpSchema, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.phone == data.phone).first()
    if existing:
        raise HTTPException(status_code=400, detail="Phone already registered")
    
    user = User(
        business_name=data.business_name,
        phone=data.phone,
        pin=data.pin
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Account created successfully", "user_id": user.id, "business_name": user.business_name}

@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == data.phone, User.pin == data.pin).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Phone or PIN")
    return {
        "message": "Login successful",
        "user_id": user.id,
        "business_name": user.business_name,
        "phone": user.phone
    }