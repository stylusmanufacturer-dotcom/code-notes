from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ....schemas.user import UserCreate, UserResponse
from ....crud.user import get_user_by_email, create_user, verify_password, user
from ....db.session import get_db
from ....core.security import create_access_token


router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        return create_user(db, user)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email = get_user_by_email(db, form_data.username)
    verify = verify_password(form_data.password, email.hashed_password)
    if not verify:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return {"access_token": create_access_token(data={"sub": email.email}, expires_delta=timedelta(minutes=10)),
            "token_type": "bearer"}




