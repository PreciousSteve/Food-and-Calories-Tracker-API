from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.crud import user_crud
from app.schemas import user_schema

from app.database.db import get_db

router = APIRouter(tags=["Auth"])


@router.post("/signup", description="Create new user")
async def sign_up(user: user_schema.Users, session: Session = Depends(get_db)):
    existing_user = user_crud.get_user_by_email(session, user.email)
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists")

    new_user = user_crud.create_user(session=session, user=user)
    return {"detail": "User Successfully Created"}
