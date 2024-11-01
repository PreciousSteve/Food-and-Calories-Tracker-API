from fastapi import APIRouter, Depends, HTTPException
from app.database.db import get_db
from app.schemas.profile_schema import Profile
from sqlalchemy.orm import Session
from app.core.auth import get_current_active_user
from app.crud.profile_crud import (
    create_profile,
    get_profile,
    update_profile,
    delete_profile,
)

router = APIRouter(tags=["Profile"])


@router.post(
    "/users/me/profile",
    description="Create a new profile or update an existing profile for the current user.",
)
def new_profile(
    profile: Profile,
    session: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    existing_profile = get_profile(session=session, user_id=current_user.id)
    if existing_profile:
        # If profile exists, update it
        for key, value in profile.model_dump().items():
            setattr(existing_profile, key, value)
        session.commit()
        session.refresh(existing_profile)
        return existing_profile
    else:
        new_profile = create_profile(
            session=session, profile=profile, user_id=current_user.id
        )
        return new_profile


@router.get(
    "/users/me/profile",
    response_model=Profile,
    description="Retrieve the profile of the current user.",
)
def read_profile(
    session: Session = Depends(get_db), current_user=Depends(get_current_active_user)
):
    profile = get_profile(session=session, user_id=current_user.id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put(
    "/users/me/edit-profile",
    response_model=Profile,
    description="Edit the profile of the current user.",
)
def edit_profile(
    profile: Profile,
    session: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    existing_profile = get_profile(session=session, user_id=current_user.id)
    if existing_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    updated_profile = update_profile(
        session=session, profile=profile, user_id=current_user.id
    )
    return updated_profile


@router.delete(
    "/users/me/delete-profile", description="Delete the profile of the current user."
)
def remove_profile(
    session: Session = Depends(get_db), current_user=Depends(get_current_active_user)
):
    profile = get_profile(session=session, user_id=current_user.id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not Found or created")
    delete_profile(session=session, user_id=current_user.id)
    return {"message": "Profile Removed Successfully"}
