from fastapi import APIRouter, HTTPException, Depends, status
from starlette.responses import JSONResponse
from starlette.background import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from sqlalchemy.orm import Session
from crud import user_crud
from schemas import user_schema
from core.auth import create_reset_password_token, decode_reset_password_token
from core.security import get_password_hash
from jinja2 import Template
from core.config import APP_HOST, FORGET_PASSWORD_URL, MAIL_FROM_NAME, FORGET_PASSWORD_LINK_EXPIRE_MINUTES, mail_conf, CustomFastMail

from database.db import get_db


APP_HOST = APP_HOST
FORGET_PASSWORD_URL  = FORGET_PASSWORD_URL
MAIL_FROM_NAME = MAIL_FROM_NAME
FORGET_PASSWORD_LINK_EXPIRE_MINUTES = FORGET_PASSWORD_LINK_EXPIRE_MINUTES

router = APIRouter(tags=["Auth"])


mail_conf = mail_conf

@router.post("/signup")
async def sign_up(user: user_schema.Users, session: Session = Depends(get_db)):
    existing_user = user_crud.get_user_by_email(session, user.email)
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists")

    new_user = user_crud.create_user(session=session, user=user)
    return {"detail": "User Successfully Created"}


@router.post("/forgot-password")
async def forgot_password(background_tasks: BackgroundTasks, fpr: user_schema.ForgetPasswordRequest, session: Session = Depends(get_db)):
    try:
        user = user_crud.get_user(email_ads=fpr.email, session=session)
        if user is None:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                  detail="Invalid Email address")
            
        secret_token = create_reset_password_token(email=user.email)

        forget_url_link =  f"{APP_HOST}{FORGET_PASSWORD_URL}/{secret_token}"
        
        email_body = { "company_name": MAIL_FROM_NAME,
                       "link_expiry_min": FORGET_PASSWORD_LINK_EXPIRE_MINUTES,
                       "reset_link": forget_url_link }
        
        def render_template(template_body):
            template_string = """
            <p>Hello,</p>
            <p>You have requested to reset your password. Please use the link below to reset it:</p>
            <a href="{{ reset_link }}">Reset Password</a>
            <p>This link will expire in {{ link_expiry_min }} minutes.</p>
            """
            template = Template(template_string)
            return template.render(template_body)

        rendered_body = render_template(email_body)
        
        

        message = MessageSchema(
            subject="Password Reset Instructions",
            recipients=[fpr.email],
            body=rendered_body,   #template_body
            subtype=MessageType.html
          )
       
        template_name = "mail/password_reset.html"


        fm = CustomFastMail(mail_conf)
        background_tasks.add_task(fm.send_message, message, template_name)
            
        return JSONResponse(status_code=status.HTTP_200_OK,
           content={"message": "Email has been sent", "success": True,
               "status_code": status.HTTP_200_OK})
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Something Unexpected: {str(e)}")



@router.post("/reset-password/{secret_token}", response_model=user_schema.SuccessMessage)
async def reset_password(secret_token, rfp: user_schema.ResetForgetPassword, session: Session = Depends(get_db)):
    try:
        info = decode_reset_password_token(token=secret_token)
        if info is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                   detail="Invalid Password Reset Payload or Reset Link Expired")
        if rfp.new_password != rfp.confirm_password:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                   detail="New password and confirm password are not same.")

        hashed_password = get_password_hash(rfp.new_password) 
        user = user_crud.get_user(email_ads=info, session=session)
        user.hashed_password = hashed_password
        session.add(user)
        session.commit()
        return {'success': True, 'status_code': status.HTTP_200_OK,
                 'message': 'Password Reset Successful!'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
              detail="Some thing unexpected happened!")