from sqlalchemy import Column, Integer, String, ForeignKey, Time, Boolean
from sqlalchemy.orm import relationship
from app.database.db import Base

class Reminder(Base):
    __tablename__="reminders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    reminder_label = Column(String)
    reminder_time = Column(Time, nullable=False)
    active = Column(Boolean, default=True)
    
    user = relationship("User", back_populates="reminder")