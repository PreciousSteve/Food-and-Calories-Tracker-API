from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session

from database.db import engine, get_db

from core.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    authenticate_user,
    get_current_active_user,
    Token,
    EmailPasswordRequestForm
)

router = APIRouter()


@router.post("/login", response_model=Token, tags=["Auth"], description="Authenticate user with email and password. Returns an access token upon successful login.")
async def login_for_access_token(form_data: Annotated[EmailPasswordRequestForm, Depends()], session: Session = Depends(get_db)):
    user = authenticate_user(session, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", tags=["Profile"], description="Fetch the user info of the authenticated user.")
async def read_users_me(current_user:Annotated[str, Depends(get_current_active_user)]):
    return {"message": f"Hello, {current_user.username}"}