from datetime import timedelta

from fastapi import APIRouter, Depends, Response, Request, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from twilio.jwt import JwtDecodeError
from jwt import ExpiredSignatureError

from core.models import db_helper
from .crud import oauth2_scheme
from .schemas import (UserCreate, VerifyCodeReturn, LoginRequest, UserSchema, VerifyCodeRequest,
                      RefreshRequest, UserUpdateSchema, ChangePasswordBody, ChangeUserSubscriptionToNews,
                      ChangePasswordWithEmail)
from . import utils as auth_utils
from . import crud

router = APIRouter(tags=["JWT Auth"])


@router.post("/signup", response_model=UserCreate, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate,
                        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_user = await crud.create_user(session, user)
    verification_code = auth_utils.generate_validation_code()

    try:
        auth_utils.send_twilio_sms(phone_number=f"+{user.phone_number}", code=verification_code)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    await crud.save_verification_code_to_redis(user.phone_number, code=verification_code)
    return UserSchema.model_validate(new_user)


@router.post("/verify-sms-code", response_model=VerifyCodeReturn, status_code=status.HTTP_200_OK)
async def verify_code(request: VerifyCodeRequest,
                      session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    stored_code = await crud.get_verification_code_from_redis(request.phone_number)

    if not stored_code or stored_code != request.code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verification code")
    await crud.delete_verification_code_from_redis(request.phone_number)

    user = await crud.get_user_by_phone_number(session, request.phone_number)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_verified = True
    session.add(user)
    await session.commit()

    access_token_expires = timedelta(minutes=30)
    refresh_token_expires = timedelta(days=7)
    access_token, refresh_token = crud.create_access_refresh_token_pair(
        data={"sub": str(user.id)},
        access_expires_delta=access_token_expires,
        refresh_expires_delta=refresh_token_expires
    )

    return {"user": user, "access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.patch("/user/update/{user_email}", response_model=UserUpdateSchema)
async def update_user(
        user_email: str,
        user_data: UserUpdateSchema = Body(...),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    user = await crud.update_user_by_email(user_email=user_email, user_data=user_data, session=session)
    return user


@router.patch("/user/change-password", status_code=status.HTTP_200_OK)
async def change_password(
        request: ChangePasswordBody,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    user = await crud.get_user_by_email(session, request.user_email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not auth_utils.validate_password(request.current_password, user.password.encode()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неправильний пароль")

    hashed_new_password = auth_utils.hash_password(request.new_password)

    user.password = hashed_new_password.decode()
    session.add(user)
    await session.commit()
    return {"message": "Password changed successfully"}


@router.patch("/user/change-password-with-email", status_code=status.HTTP_200_OK)
async def change_password_with_email(
        request: ChangePasswordWithEmail,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    user = await crud.get_user_by_email(session, str(request.user_email))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    try:
        random_password = auth_utils.generate_user_random_password()
        sending_status = await auth_utils.send_user_password_to_email([request.user_email], random_password)
        if sending_status:
            hashed_password = auth_utils.hash_password(random_password)
            user.password = hashed_password.decode()
            session.add(user)
            await session.commit()
            return {"message": f"Email has been sent to {request.user_email} with status: {sending_status}"}
        else:
            return {"message": "Error changing password"}
    except Exception as e:
        return {"error": str(e)}


@router.patch("/user/subscribe-to-news", status_code=status.HTTP_200_OK)
async def subscribe_user_to_news(
        request: ChangeUserSubscriptionToNews,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    user = await crud.get_user_by_phone_number(session, request.phone_number)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_subscribed_to_news = request.is_subscribed_to_news
    session.add(user)
    await session.commit()
    return {"message": f"User: {'subscribed' if user.is_subscribed_to_news else 'unsubscribed'} to news"}


@router.post("/jwt/login")
async def login_for_access_token(
        login: LoginRequest,
        response: Response,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    user = await crud.authenticate_user(email=login.email, password=login.password, session=session)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Неправильний логін чи пароль",
                            headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=30)
    refresh_token_expires = timedelta(days=7)

    access_token, refresh_token = crud.create_access_refresh_token_pair(data={"sub": str(user.id)},
                                                                        access_expires_delta=access_token_expires,
                                                                        refresh_expires_delta=refresh_token_expires)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=1800,
        path="/",
        secure=False,
        samesite="lax",
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,
        samesite="lax",
    )
    return {"user": user}


@router.get("/by-email/{user_email}")
async def get_user_by_email(user_email: str,
                         session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    user = await crud.get_user_by_email(session, user_email)
    return user


@router.get("/jwt/verify-token")
async def verify_access_token(
        request: Request,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authenticated")

    try:
        payload = auth_utils.decode_jwt(token)
        user_id = int(payload.get("sub"))
        user = await crud.get_user_by_id(session, user_id)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        if user.email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return {"status": "success", "email": user.email}
    except JwtDecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid_token")
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token")


@router.post("/jwt/refresh")
async def refresh_access_token(response: Response,
                               request: Request,
                               session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authenticated")

    try:
        payload = auth_utils.decode_jwt(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        user_id = int(payload["sub"])
        user = await crud.get_user_by_id(session, int(user_id))

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        access_token_expires = timedelta(minutes=30)
        access_token, _ = crud.create_access_refresh_token_pair(data={"sub": str(user.id)},
                                                                access_expires_delta=access_token_expires,
                                                                refresh_expires_delta=timedelta(days=7))
        response.set_cookie(
            "access_token",
            value=access_token,
            httponly=True,
            max_age=1800,
            samesite="lax",
        )
        return {"message": "refreshed"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid refresh token {e}")


@router.post("/jwt/logout", status_code=status.HTTP_200_OK)
async def logout_user(
        request: Request,
        response: Response,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    refresh_token = request.cookies.get("refresh_token")
    try:
        payload = auth_utils.decode_jwt(refresh_token)

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        user = await crud.get_user_by_id(session, int(user_id))

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return {"message": "Successfully logged out"}

    except JwtDecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired token"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during logout: {e}"
        )
