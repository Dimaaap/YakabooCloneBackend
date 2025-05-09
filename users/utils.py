import random
import os
from pathlib import Path
from datetime import datetime, timedelta
from string import ascii_letters, digits

from fastapi_mail import MessageSchema, MessageType, FastMail, ConnectionConfig
import bcrypt
import jwt
from fastapi import HTTPException
from pydantic import EmailStr
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
from dotenv import load_dotenv

from core.config import settings

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS") == "True",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS") == "True",
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=str(Path(__file__).parent / "templates" / "email_templates")
)


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire,
                     iat=now)
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm
    )
    return encoded


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm]
    )
    return decoded


def generate_validation_code():
    return str(random.randint(100_000, 999_999))


def generate_user_random_password():
    password_len = int(os.getenv("RANDOM_PASSWORD_LENGTH"))
    chars = ascii_letters + digits
    password = "".join(random.sample(chars, password_len))
    return password


async def send_user_password_to_email(list_emails: list[EmailStr], password: str):
    message = MessageSchema(
        subject="Ваш новий пароль",
        recipients=list_emails,
        template_body={"password": password},
        subtype=MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="new_password.html")
    return True


def send_twilio_sms(phone_number: str, code: str):
    twilio_account_id, twilio_auth_token = os.getenv("TWILIO_ACCOUNT_ID"), os.getenv("TWILIO_AUTH_TOKEN")
    twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
    client = Client(twilio_account_id, twilio_auth_token)

    try:
        message = client.messages.create(
            body=f"Ваш код підтвердження: {code}",
            from_=twilio_phone_number,
            to=phone_number
        )
    except TwilioRestException as e:
        raise HTTPException(status_code=500, detail=f"Twilio error: {e}")
    return message.sid


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)

