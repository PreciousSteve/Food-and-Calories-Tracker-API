from pydantic import BaseModel
from typing import Optional

class Food(BaseModel):
    name:str	             # ex = oatmeal
    serving_size:str	     # ex = 100 grams
    kcal_per_serving:int     # ex = 336
    # kcal = calories. You can find the calories per serving on the nutrition label of your food item. if unsure, use an online calorie calculator or database.
    protein_grams:float	     # ex = 13.2
    fibre_grams:float = 0    # ex = 10.1
    
    
class FoodResponse(BaseModel):
    id: int
    name: str
    serving_size: str
    kcal_per_serving: int
    protein_grams: float
    fibre_grams: Optional[float] = None
    user_id: int
    profile_id: Optional[int] = None

    class Config:
        orm_mode = True