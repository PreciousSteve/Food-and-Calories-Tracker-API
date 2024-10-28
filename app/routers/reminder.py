from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.reminder_schema import Reminder
from app.database.db import get_db
from app.core.auth import get_current_active_user
from app.crud.reminder_crud import (
    create_reminder,
    update_reminder,
    get_reminder_by_id,
    get_reminders,
    delete_reminder,
)

router = APIRouter(tags=["Reminder"])


@router.post(
    "/reminder", description="Create reminder for the currently authenticated user."
)
def add_reminder(
    reminder: Reminder,
    session: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    This endpoint allows the authenticated user to create a reminder.
    - reminder: The new details of the reminder.
    - session: Current database session.
    - current_user: The user making the request.
    - Returns a successful message.
    """
    create_reminder(
        session=session, reminder=reminder, user_id=current_user.id
    )

    return {"message": "Reminder set successfully"}


@router.get(
    "/reminders", description="Get all reminders for the currently authenticated user."
)
def get_all_reminders(
    session: Session = Depends(get_db), current_user=Depends(get_current_active_user)
):
    """
    This endpoint retrieves all reminders for the logged-in user.
    - session: Current database session.
    - current_user: The user making the request.
    - Returns a list of reminders.
    """
    reminders = get_reminders(session=session, user_id=current_user.id)
    if not reminders:
        raise HTTPException(status_code=404, detail="No reminder created")
    return reminders


@router.get(
    "/reminder/{reminder_id}",
    description="Get reminder based on reminder ID for the currently authenticated user.",
)
def get_reminder(
    reminder_id: int,
    session: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    This endpoint retrieves a reminder for a logged-in user by its ID.
    - **reminder_id**: ID of the reminder to be updated.
    - **session**: Current database session.
    - **current_user**: The user making the request.
    - Returns the reminder object.
    """
    reminder = get_reminder_by_id(session=session, reminder_id=reminder_id)
    if reminder is None:
        raise HTTPException(status_code=404, detail="Reminder not found")
    if reminder.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return reminder


@router.put(
    "/reminder/{reminder_id}",
    response_model=Reminder,
    description="Edit a specific reminder by its ID.",
)
def edit_reminder(
    reminder_id: int,
    reminder: Reminder,
    session: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    This endpoint allows the authenticated user to edit a reminder by its ID.
    - **reminder_id**: ID of the reminder to be updated.
    - **reminder**: The new details of the reminder.
    - **session**: Current database session.
    - **current_user**: The user making the request.
    - Returns the updated reminder object.
    """
    existing_reminder = get_reminder_by_id(session=session, reminder_id=reminder_id)
    if existing_reminder is None:
        raise HTTPException(status_code=404, detail="Reminder not found")
    if existing_reminder.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to edit this reminder"
        )

    updated_reminder = update_reminder(
        session=session, existing_reminder=existing_reminder, reminder=reminder
    )

    return updated_reminder


@router.delete(
    "/reminder/{reminder_id}", description="Delete a specific reminder by its ID"
)
def remove_reminder(
    reminder_id: int,
    session: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    existing_reminder = get_reminder_by_id(session=session, reminder_id=reminder_id)
    if existing_reminder is None:
        raise HTTPException(status_code=404, detail="Reminder not found")
    if existing_reminder.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this data"
        )
    delete_reminder(session=session, reminder_id=reminder_id)

    return {"message": "Reminder deleted"}
