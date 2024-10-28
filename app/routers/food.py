from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.food import Food, FoodResponse
from app.database.db import get_db
from app.crud.food import (
    create_food,
    get_food,
    get_food_by_id,
    get_food_by_name,
    edit_food,
    delete_food,
    get_user_total_calories,
)
from app.core.auth import get_current_active_user

router = APIRouter(tags=["Food"])


@router.post(
    "/food",
    response_model=FoodResponse,
    description="allows users who created their profile to add new food entries.",
)
def add_food(
    food: Food,
    session: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    new_food = create_food(session=session, food=food, user_id=current_user.id)
    if not new_food.profile_id:
        raise HTTPException(status_code=404, detail="Profile not found for the user")

    return new_food


@router.get(
    "/foods",
    description="retrieves all food entries for the authenticated user.",
)
def read_foods(
    session: Session = Depends(get_db), current_user=Depends(get_current_active_user)
):
    foods = get_food(session=session, user_id=current_user.id)
    if not foods:
        raise HTTPException(status_code=404, detail="Food data not created")
    return foods


@router.get("/food/{food_id}", description="retrieves a specific food entry by its ID.")
def read_food_by_id(
    food_id: int,
    session: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    food = get_food_by_id(session=session, food_id=food_id)
    if food is None:
        raise HTTPException(status_code=404, detail="Food data not found")
    if food.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this data"
        )
    return food


@router.get("/foods/search", description="Retrieves or search for food entries by name")
def search_food(
    name: str = Query(),
    session: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    food = get_food_by_name(session=session, name=name, user_id=current_user.id)
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    return food


@router.put(
    "/foods/{food_id}",
    description="allows users to update an existing food entry by its ID.",
)
def update_food(
    food_id: int,
    food: Food,
    session=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    existing_food = get_food_by_id(session=session, food_id=food_id)
    if existing_food is None:
        raise HTTPException(status_code=404, detail="Food data not found")
    if existing_food.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this food data"
        )

    updated_food = edit_food(session=session, food_id=food_id, food=food)
    return updated_food


@router.delete(
    "/foods/{food_id}", description="deletes a specific food entry by its ID."
)
def remove_food(
    food_id: int, session=Depends(get_db), current_user=Depends(get_current_active_user)
):
    existing_food = get_food_by_id(session=session, food_id=food_id)
    if existing_food is None:
        raise HTTPException(status_code=404, detail="Food data not found")
    if existing_food.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this food data"
        )

    delete_food(session=session, food_id=food_id)
    return {"message": "Data Deleted Successfully"}


@router.get(
    "/foods/total-calories",
    description="calculates and returns the total calories consumed",
)
def total_calories(
    session: Session = Depends(get_db), current_user=Depends(get_current_active_user)
):
    total = get_user_total_calories(session=session, user_id=current_user.id)
    return {"total_calories": total}
