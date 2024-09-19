# Writing a simple API to track food / calories using the awesome FastAPI framework. 
from fastapi import FastAPI

from .routers import food, signup, login, daily_calorie_goal, profile, reminder, password_reset
from .database.db import engine, Base


app = FastAPI(title="Food and Calorie Tracker API",
    description="API to track food intake and calories, manage user profiles, and set fitness goals.",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)


app.include_router(food.router)
app.include_router(signup.router)
app.include_router(login.router)
app.include_router(daily_calorie_goal.router)
app.include_router(profile.router)
app.include_router(reminder.router)
app.include_router(password_reset.router)


