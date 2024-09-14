from pydantic import BaseModel
from datetime import date

class Profile(BaseModel):
    first_name:str
    last_name:str
    bio:str
    date_of_birth: date
    gender:str
    weight:str
    goal_weight:str
    medical_condition:str
    fitness_goal:str
    
    class config:
        orm_mode=True