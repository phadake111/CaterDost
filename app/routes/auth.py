from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import User

router = APIRouter()


class LoginRequest(BaseModel):
    phone_number: str
    pin: str


class RegisterRequest(BaseModel):
    phone_number: str
    pin: str
    name: str | None = None


@router.post("/signup")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.phone == data.phone_number).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this phone number already exists"
            )

        new_user = User(
            phone=data.phone_number,
            pin=data.pin,
            name=data.name
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "User registered successfully", "user_id": new_user.id}
    except HTTPException as e:
        raise e
    except Exception as err:
        db.rollback()
        print(f"REGISTER ERROR: {str(err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error during registration: {str(err)}"
        )


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        # Check if user exists in database
        user = db.query(User).filter(User.phone == data.phone_number).first()
        
        if not user or user.pin != data.pin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid phone number or PIN"
            )

        return {
            "message": "Login successful",
            "access_token": f"token-{user.id}",
            "user": {
                "id": user.id,
                "phone": user.phone,
                "name": getattr(user, "name", None)
            }
        }
    except HTTPException as e:
        raise e
    except Exception as err:
        print(f"LOGIN ERROR: {str(err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error during login: {str(err)}"
        )