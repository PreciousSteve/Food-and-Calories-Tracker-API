from sqlalchemy import Column, String, Integer, Float, ForeignKey
from database.db import Base
from sqlalchemy.orm import relationship

class Food(Base):
    __tablename__ ="foods"
    
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String, index=True)	 # ex = oatmeal
    serving_size = Column(String)	     # ex = 100 grams
    kcal_per_serving= Column(Integer)    # ex = 336
    # kcal = calories	
    protein_grams = Column(Float)     # ex = 13.2
    fibre_grams = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    profile_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)
    
    user = relationship("User", back_populates="foods")
    profile = relationship("Profile", back_populates="foods")
