from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.reminder_schema import Reminder
from database.db import get_db
from core.auth import get_current_active_user
from crud.reminder_crud import create_reminder, update_reminder, get_reminder_by_id, get_reminders

router = APIRouter(tags=["Reminder"])

@router.post("/reminder")
def add_reminder(reminder: Reminder, session:Session=Depends(get_db), current_user=Depends(get_current_active_user)):
    new_reminder = create_reminder(session=session, reminder=reminder, user_id = current_user.id)
    
    return {"message":"Reminder set successfully"}


@router.get("/reminders")
def get_all_reminders(session: Session=Depends(get_db), current_user=Depends(get_current_active_user)):
    reminders = get_reminders(session=session, user_id =current_user.id)
    if not reminders:
        raise HTTPException(status_code=404, detail="No reminder created")
    return reminders


@router.get("/reminder/{reminder_id}")
def get_reminder(reminder_id:int, session:Session=Depends(get_db), current_user=Depends(get_current_active_user)):
    reminder = get_reminder_by_id(session=session, reminder_id=reminder_id)
    if reminder is None:
        raise HTTPException(status_code=404, detail="Reminder not found")
    if reminder.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return reminder


@router.put("/edit-reminder/{reminder_id}", response_model=Reminder)
def edit_reminder(reminder_id: int, reminder: Reminder, session: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    existing_reminder = get_reminder_by_id(session=session, reminder_id=reminder_id)
    if existing_reminder is None:
        raise HTTPException(status_code=404, detail="Reminder not found")
    if existing_reminder.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this reminder")

    updated_reminder = update_reminder(session=session, existing_reminder=existing_reminder, reminder=reminder)
    
    return updated_reminder