from models import food_model, profile_model
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import func
from schemas.food import Food


def create_food(session:Session, food:Food, user_id:int):
    profile = session.query(profile_model.Profile).filter(profile_model.Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found for the user")

    new_food = food_model.Food(name=food.name, serving_size=food.serving_size,
                         kcal_per_serving=food.kcal_per_serving,
                         protein_grams=food.protein_grams,
                         fibre_grams=food.fibre_grams, user_id=user_id, profile_id=profile.id )
    session.add(new_food)
    session.commit()
    session.refresh(new_food)
    
        
    return new_food
    
    
def get_food(session:Session, user_id:int):
    return session.query(food_model.Food).filter(food_model.Food.user_id == user_id).all()
    

def get_food_by_id(session: Session, food_id:int):
    return session.query(food_model.Food).filter(food_model.Food.id == food_id).first()


def get_food_by_name(session: Session, name: str,  user_id: int):
    return session.query(food_model.Food).filter(food_model.Food.name == name, food_model.Food.user_id == user_id).first()


def edit_food(session: Session, food_id: int, food: Food):
    add_edit = session.query(food_model.Food).filter(food_model.Food.id == food_id).first()
    if not add_edit:
        return None
    for key, value in food.model_dump().items():
        setattr(add_edit, key, value)
    session.commit()
    session.refresh(add_edit)
    return add_edit

def delete_food(session: Session, food_id: int):
    food = session.query(food_model.Food).filter(food_model.Food.id == food_id).first()
    if not food:
        return None
    session.delete(food)
    session.commit()
    return food


def get_user_total_calories(session: Session, user_id:int):
    total_calories = session.query(func.sum(food_model.Food.kcal_per_serving)).filter(food_model.Food.user_id == user_id).scalar()
    return total_calories or 0