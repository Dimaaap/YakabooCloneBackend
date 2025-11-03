from datetime import timedelta, datetime

import sqlalchemy
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import redis_client
from . import utils as auth_utils
from .schemas import UserCreate, UserUpdateSchema
from core.models import User, Cart

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/jwt/login")


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    statement = select(User).filter(User.email == email)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    statement = select(User).filter(User.id == user_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_user_by_phone_number(session: AsyncSession, phone_number: str) -> User | None:
    statement = select(User).filter(User.phone_number == phone_number)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def check_user_existing(session: AsyncSession, user_email: str, phone_number: str) -> None:
    user_with_email_exists = await get_user_by_email(session, user_email)
    user_with_phone_number_exists = await get_user_by_phone_number(session, phone_number)

    if user_with_email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Користувач з таким email уже зареєстрований"
        )

    if user_with_phone_number_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Користувач з таким номером телефону вже зареєстрований"
        )
    return None


async def create_user(session: AsyncSession, user: UserCreate):
    hashed_password = auth_utils.hash_password(user.password)
    await check_user_existing(session, user.email, user.phone_number)

    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        email=user.email,
        password=hashed_password.decode()
    )

    db_user.cart = Cart()
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def update_user_by_email(user_email: str, user_data: UserUpdateSchema, session: AsyncSession):
    user = await get_user_by_email(session, user_email)
    conflict_field = None
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {user_email} not found")

    try:
        for field, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
            conflict_field = field
        await session.commit()
        await session.refresh(user)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Unique constraint: {conflict_field}")
    return user


async def authenticate_user(email: str, password: str, session: AsyncSession) -> User | bool:
    statement = select(User).filter(User.email == email)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        return False
    if not auth_utils.validate_password(password, user.password.encode()):
        print("Password not valid")
        return False
    return user


async def save_verification_code_to_redis(phone_number: str, code: str):
    await redis_client.set(f"ver_code:{phone_number}", code)


async def get_verification_code_from_redis(phone_number: str) -> bytes:
    return await redis_client.get(f"ver_code:{phone_number}")


async def delete_verification_code_from_redis(phone_number: str):
    await redis_client.delete(f"ver_code:{phone_number}")


def create_access_refresh_token_pair(data: dict, access_expires_delta: timedelta | None = None,
                                     refresh_expires_delta: timedelta | None = None):
    to_encode = data.copy()
    access_expire = datetime.utcnow() + access_expires_delta
    refresh_expires = datetime.utcnow() + refresh_expires_delta
    to_encode.update({"exp": access_expire})
    access_token = auth_utils.encode_jwt(to_encode)

    to_encode.update({"exp": refresh_expires, "type": "refresh"})
    refresh_token = auth_utils.encode_jwt(to_encode, expire_timedelta=refresh_expires_delta)
    return access_token, refresh_token