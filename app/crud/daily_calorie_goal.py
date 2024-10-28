from app.models import daily_calorie_model
from sqlalchemy.orm import Session
from app.schemas.daily_calorie_goal import CalorieGoal


def create_calorie_goal(session: Session, goal: CalorieGoal, user_id: int):
    new_goal = daily_calorie_model.DailyCalorieGoal(calorie_goal=goal.calorie_goal, user_id=user_id)
    session.add(new_goal)
    session.commit()
    session.refresh(new_goal)
    return new_goal


def get_calorie_goal(session: Session, user_id: int):
    return session.query(daily_calorie_model.DailyCalorieGoal).filter(
        daily_calorie_model.DailyCalorieGoal.user_id == user_id).first()
