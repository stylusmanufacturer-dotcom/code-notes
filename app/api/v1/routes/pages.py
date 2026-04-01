

from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from ....core.security import verify_token
from ....crud.note import get_notes
from ..dependencies.auth import get_current_user
from ....crud.user import get_user_by_email, create_user
from ....db.session import get_db
from ....core.templating import templates

from fastapi import APIRouter, Depends, Request

router = APIRouter()

@router.get("/")
def render_notes(request: Request,db: Session = Depends(get_db)):
    try:
        token = request.cookies.get("access_token")
        current_user = verify_token(token)
        user = get_user_by_email(db, email = current_user)
        notes = get_notes(db, user.id)
        return templates.TemplateResponse(request=request, name="notes.html", context={"notes": notes})
    except Exception as e:
        print(f"Error: {e}")
        return RedirectResponse(url="/login")

@router.get("/login/")
def render_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@router.get("/register/")
def render_register(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")

