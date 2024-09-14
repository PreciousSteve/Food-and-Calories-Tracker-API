from sqlalchemy import Column, String, Integer, Boolean
from database.db import Base
from sqlalchemy.orm import relationship
from models.profile_model import Profile

class User(Base):
    __tablename__="users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    foods = relationship("Food", back_populates="user")
    calorie_goal = relationship("DailyCalorieGoal", back_populates="user")
    profile = relationship("Profile", back_populates="user", uselist=False, foreign_keys=[Profile.user_id])