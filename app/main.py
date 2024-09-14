# Writing a simple API to track food / calories using the awesome FastAPI framework. 
from fastapi import FastAPI

from routers import food, signup, login, daily_calorie_goal, profile
from database.db import engine, Base


app = FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(food.router)
app.include_router(signup.router)
app.include_router(login.router)
app.include_router(daily_calorie_goal.router)
app.include_router(profile.router)



