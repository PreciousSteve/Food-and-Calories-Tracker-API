import os
from dotenv import load_dotenv
from fastapi_mail import FastMail, ConnectionConfig
from aiosmtplib.errors import SMTPResponseException

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


APP_HOST = os.getenv("APP_HOST")
FORGET_PASSWORD_URL  = os.getenv("FORGET_PASSWORD_URL")
MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")
FORGET_PASSWORD_LINK_EXPIRE_MINUTES = os.getenv("FORGET_PASSWORD_LINK_EXPIRE_MINUTES")

def str_to_bool(value):
    return value.lower() in ("true", "1", "t", "yes", "y", "on")

required_vars = ["MAIL_USERNAME", "MAIL_PASSWORD", "MAIL_SERVER", "MAIL_FROM"]
for var in required_vars:
    if os.getenv(var) is None:
        raise ValueError(f"Required environment variable {var} is not set")
    

mail_conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_PORT =int(os.getenv("MAIL_PORT", 2525)),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_STARTTLS=str_to_bool(os.getenv("MAIL_STARTTLS", "True")),
    MAIL_SSL_TLS=str_to_bool(os.getenv("MAIL_SSL_TLS", "False")),
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

class CustomFastMail(FastMail):
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.session.quit()
        except SMTPResponseException as e:
            if e.code == 250 and e.message == "OK":
                pass
            else:
                raise e