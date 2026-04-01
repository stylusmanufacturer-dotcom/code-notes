from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ....schemas.user import UserCreate, UserResponse
from ....crud.user import get_user_by_email, create_user, verify_password, user
from ....db.session import get_db
from ....core.security import create_access_token
from fastapi.responses import RedirectResponse
from fastapi import Form
router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, email=email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_data = UserCreate(email=email, password=password)
    return create_user(db, user_data)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print("username recieved: ", form_data.username)
    email = get_user_by_email(db, form_data.username)
    print("email recieved: ", email)
    verify = verify_password(form_data.password, email.hashed_password)
    if not verify:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token(data={"sub": email.email}, expires_delta=timedelta(minutes=30))

    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="access_token", value=token, httponly=True)


    return response