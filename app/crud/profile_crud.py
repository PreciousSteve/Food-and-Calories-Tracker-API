from models import profile_model, food_model
from sqlalchemy.orm import Session
from schemas.profile_schema import Profile


def get_profile(session: Session, user_id: int):
    return session.query(profile_model.Profile).filter(profile_model.Profile.user_id == user_id).first()


def create_profile(session: Session, profile:Profile, user_id:int):
    new_profile = profile_model.Profile(first_name=profile.first_name, last_name=profile.last_name, bio=profile.bio,
                                    date_of_birth=profile.date_of_birth, gender=profile.gender, weight=profile.weight,
                                    goal_weight=profile.goal_weight, medical_condition=profile.medical_condition, fitness_goal=profile.fitness_goal, user_id = user_id)
    session.add(new_profile)
    session.commit()
    session.refresh(new_profile)
    

    return new_profile


def update_profile(session: Session, user_id:int, profile:Profile):
    searched_profile = session.query(profile_model.Profile).filter(profile_model.Profile.user_id == user_id).first()
    if not searched_profile:
        return None
    for key, value in profile.model_dump().items():
        setattr(searched_profile, key, value)
    session.commit()
    session.refresh(searched_profile)
    return searched_profile
            
        
def delete_profile(session: Session, user_id:int):
    profile = session.query(profile_model.Profile).filter(profile_model.Profile.user_id == user_id).first()
    if not profile:
        return None
    session.delete(profile)
    session.commit()
    return profile