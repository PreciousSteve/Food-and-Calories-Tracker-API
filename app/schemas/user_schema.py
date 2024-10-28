from pydantic import BaseModel, Field, field_validator
from typing import Any


class FormData(BaseModel):
    email: str
    password: str


class ForgetPasswordRequest(BaseModel):
    email: str


class ResetForgotPassword(BaseModel):
    new_password: str
    confirm_password: str

    @field_validator("new_password")
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.islower() for c in value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one digit")
        if not any(c in "!@#$%^&*()-_+=" for c in value):
            raise ValueError("Password must contain at least one special character")
        return value

    @field_validator("confirm_password")
    def passwords_match(cls, value: str, info: Any) -> str:
        if "new_password" in info.data and value != info.data["new_password"]:
            raise ValueError("New Password and confirm password do not match")
        return value


class SuccessMessage(BaseModel):
    success: bool
    status_code: int
    message: str


class Users(BaseModel):
    username: str = Field(max_length=10)
    email: str
    password: str
    confirm_password: str

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.islower() for c in value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one digit")
        if not any(c in "!@#$%^&*()-_+=" for c in value):
            raise ValueError("Password must contain at least one special character")
        return value

    @field_validator("confirm_password")
    def passwords_match(cls, value: str, info: Any) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Password and confirm password do not match")
        return value
