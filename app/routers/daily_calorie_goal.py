from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from core.auth import get_current_active_user
from schemas.daily_calorie_goal import CalorieGoal 
from crud.daily_calorie_goal import create_calorie_goal, get_calorie_goal
from crud.food import get_user_total_calories

router = APIRouter()

@router.post("/users/me/calorie-goal")
def set_calorie_goal(goal:CalorieGoal, session:Session=Depends(get_db), current_user = Depends(get_current_active_user)):
    existing_goal = get_calorie_goal(session=session, user_id=current_user.id)
    if existing_goal:
        existing_goal.calorie_goal = goal.calorie_goal
        session.commit()
        session.refresh(existing_goal)
        return existing_goal
    else:
        new_goal = create_calorie_goal(session=session, goal=goal, user_id=current_user.id)
    
        return {"message": "Daily calorie goal set successfully."}


@router.get("/users/me/calorie-goal")
def get_goal(session:Session=Depends(get_db), current_user=Depends(get_current_active_user)):
    goal = get_calorie_goal(session=session, user_id=current_user.id)
    if goal is None: 
        raise HTTPException(status_code=404, detail="Calorie goal not set")
    return goal


@router.get("/users/me/calorie-goal-progress")
def get_caloric_goal_progress(session: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    total_calories = get_user_total_calories(session, current_user.id)
    calorie_goal_record = get_calorie_goal(session, current_user.id)
    if calorie_goal_record is None:
        raise HTTPException(status_code=404, detail="Error! Calorie Goal not set")
    calorie_goal = calorie_goal_record.calorie_goal
    if total_calories < calorie_goal :
        return {
            "status": "Under goal",
            "calories_consumed": total_calories,
            "caloric_goal": calorie_goal,
            "calories_remaining": calorie_goal - total_calories
        }
    elif total_calories == calorie_goal:
        return {
            "status": "Goal met",
            "calories_consumed": total_calories,
            "caloric_goal": calorie_goal,
            "calories_remaining": 0
        }
    else:
        return {
            "status": "Over goal",
            "calories_consumed": total_calories,
            "caloric_goal": calorie_goal,
            "calories_over": total_calories - calorie_goal
        }
    
