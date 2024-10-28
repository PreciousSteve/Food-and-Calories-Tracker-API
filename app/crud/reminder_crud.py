from app.models import reminder_model
from sqlalchemy.orm import Session
from app.schemas.reminder_schema import Reminder


def create_reminder(session: Session, reminder: Reminder, user_id: int):
    new_reminder = reminder_model.Reminder(
        reminder_label=reminder.reminder_label,
        reminder_time=reminder.reminder_time,
        active=reminder.active,
        user_id=user_id,
    )
    session.add(new_reminder)
    session.commit()
    session.refresh(new_reminder)
    return new_reminder


def get_reminders(session: Session, user_id: int):
    return (
        session.query(reminder_model.Reminder)
        .filter(reminder_model.Reminder.user_id == user_id)
        .all()
    )


def get_reminder_by_id(session: Session, reminder_id: int):
    return (
        session.query(reminder_model.Reminder)
        .filter(reminder_model.Reminder.id == reminder_id)
        .first()
    )


def update_reminder(session: Session, existing_reminder, reminder: Reminder):
    existing_reminder.reminder_label = reminder.reminder_label
    existing_reminder.reminder_time = reminder.reminder_time
    existing_reminder.active = reminder.active
    session.commit()
    session.refresh(existing_reminder)
    return existing_reminder


def delete_reminder(session: Session, reminder_id: int):
    reminder = (
        session.query(reminder_model.Reminder)
        .filter(reminder_model.Reminder.id == reminder_id)
        .first()
    )
    if not reminder:
        return None
    session.delete(reminder)
    session.commit()
    return reminder
