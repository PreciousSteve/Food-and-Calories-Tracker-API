from sqlalchemy import Column, Integer, String, ForeignKey, Date
from database.db import Base
from sqlalchemy.orm import relationship

class Profile(Base):
    __tablename__="user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, nullable=False)
    bio = Column(String)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String)
    weight = Column(String)
    goal_weight = Column(String)
    medical_condition = Column(String)
    fitness_goal = Column(String)
    
    user = relationship("User", back_populates="profile")
    foods = relationship("Food", back_populates="profile")