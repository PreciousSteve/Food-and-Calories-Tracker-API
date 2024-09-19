from fastapi import APIRouter, HTTPException, status, Depends
from schemas import user_schema
from jose import JWTError, ExpiredSignatureError
from sqlalchemy.orm import Session
from database.db import get_db
from core.security import get_password_hash
from crud import user_crud
from core.auth import create_reset_password_token, decode_reset_password_token
from core.security import get_password_hash
from core.config import APP_HOST, FORGET_PASSWORD_URL, SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

router = APIRouter(tags={"Auth"})

SMTP_SERVER = SMTP_SERVER
SMTP_PORT = SMTP_PORT
SENDER_EMAIL = SENDER_EMAIL
SENDER_PASSWORD = SENDER_PASSWORD

def send_email(recipient_email: str, subject: str, body: str, html_body:str = None):
    try:
        # Set up the SMTP server and login
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Create the email
        msg = MIMEMultipart("alternative")  # "alternative" to allow both plain text and HTML
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Add plain text part
        msg.attach(MIMEText(body, 'plain'))

        # Add HTML part if provided
        if html_body:
            msg.attach(MIMEText(html_body, 'html'))

        # Send the email
        server.send_message(msg)

        # Close the connection to the server
        server.quit()

        print(f"Email sent to {recipient_email}!")

    except Exception as e:
        print(f"Failed to send email: {e}")


html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Password Reset</title>
</head>
<body>
    <h2>Password Reset Request</h2>
    <p>Hello,</p>
    <p>You requested to reset your password. Click the link below to reset your password:</p>
    <a href="{reset_url}">Reset Password</a>
    <p>This reset link expires in 10 minutes.<p>
    <p>If you did not request this, please ignore this email.</p>
</body>
</html>
"""


@router.post("/forgot-password", description="generate a mail when user forgets their password")
async def forgot_password(request: user_schema.ForgetPasswordRequest, session:Session=Depends(get_db)):
    user = user_crud.get_user(email_ads=request.email, session=session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email address")
    
    reset_token = create_reset_password_token(email=user.email)
    reset_url = f"{APP_HOST}{FORGET_PASSWORD_URL}/{reset_token}"
    
    plain_text_body = f"Hello, you requested to reset your password. Click the link to reset your password: {reset_url}"
    html_body = html_template.format(reset_url=reset_url)

    send_email(request.email, "Password Reset Request", plain_text_body, html_body)

    return {"message": "Password reset email sent!"}


@router.post("/reset-password/{token}", response_model=user_schema.SuccessMessage, description="allows a user to reset their password using a valid token sent via email")
async def reset_password(token, rp:user_schema.ResetForgotPassword, session:Session=Depends(get_db)):
    try:
        info = decode_reset_password_token(token=token)
        if info is None:
            raise HTTPException(status_code=status.HTTP_400_INTERNAL_SERVER_ERROR,
                   detail="Invalid Password Reset Payload or Reset Link Expired")
        if rp.new_password != rp.confirm_password:
            raise HTTPException(status_code=status.HTTP_400_INTERNAL_SERVER_ERROR, detail="New password and confirm password are not the same")
        
        hashed_password = get_password_hash(rp.new_password)
        user = user_crud.get_user(email_ads=info, session=session)
        user.hashed_password = hashed_password
        session.add(user)
        session.commit()
        return {'success': True, 'status_code': status.HTTP_200_OK,
                 'message': 'Password Reset Successful!'}
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token has expired"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token is invalid"
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
              detail="Token has Expired or Something unexpected happened!")