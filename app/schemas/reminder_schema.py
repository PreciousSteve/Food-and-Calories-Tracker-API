from pydantic import BaseModel
from datetime import time
from typing import Optional


class Reminder(BaseModel):
    reminder_label: str
    reminder_time: time
    active: Optional[bool] = True

    class Config:
        orm_mode = True
