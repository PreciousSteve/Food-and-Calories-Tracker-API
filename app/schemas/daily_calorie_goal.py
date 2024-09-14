from pydantic import BaseModel

# Schema for creating a new daily calorie goal
class CalorieGoal(BaseModel):
    calorie_goal: int
    
    class Config:
        orm_mode = True
    
    
class CaloricGoalResponse(BaseModel):
    id: int
    user_id: int
    calorie_goal: int

    class Config:
        orm_mode = True