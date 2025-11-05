from fastapi import APIRouter, Form
from database import register_user, verify_user

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    user = verify_user(email, password)
    return {"success": bool(user), "user": user}

@router.post("/register")
def register(email: str = Form(...), password: str = Form(...)):
    success = register_user(email, password)
    return {"success": success}
