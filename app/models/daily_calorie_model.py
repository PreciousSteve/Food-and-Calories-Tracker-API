from sqlalchemy import Column, Integer, ForeignKey
from app.database.db import Base
from sqlalchemy.orm import relationship


class DailyCalorieGoal(Base):
    __tablename__ = "daily_calorie_goals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    calorie_goal = Column(Integer, nullable=False)
    user = relationship("User", back_populates="calorie_goal")
