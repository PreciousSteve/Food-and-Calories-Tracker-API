import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


APP_HOST = os.getenv("APP_HOST")
FORGET_PASSWORD_URL  = os.getenv("FORGET_PASSWORD_URL")
MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")


