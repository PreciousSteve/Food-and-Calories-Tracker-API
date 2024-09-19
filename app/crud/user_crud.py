from app.models import user_model
from sqlalchemy.orm import Session
from app.core.security import get_password_hash

def create_user(session: Session, user):
    hashed_password = get_password_hash(user.password)
    new_user=user_model.User(username=user.username, email=user.email, hashed_password=hashed_password)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return new_user

def get_user_by_email(session: Session, email:str):
    user = session.query(user_model.User).filter(user_model.User.email == email).first()
    return user

def get_user_by_username(session:Session, username:str):
    user = session.query(user_model.User).filter(user_model.User.username == username).first()
    return user


def get_user(email_ads: str, session: Session):
    # Query the database for a user with the given email address
    user = session.query(user_model.User).filter(user_model.User.email == email_ads).first()
    return user