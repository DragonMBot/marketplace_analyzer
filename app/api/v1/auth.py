from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from app.schemas.auth import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenPair,
)

from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Регистрация пользователя.
    """

    service = AuthService(db)

    user = await service.register_user(
        email=payload.email,
        password=payload.password,
    )

    return {
        "id": user.id,
        "email": user.email,
        "message": "User created successfully",
    }


@router.post(
    "/login",
    response_model=TokenPair,
)
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Авторизация пользователя.
    """

    service = AuthService(db)

    result = await service.login(
        payload.email,
        payload.password,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return result


@router.post(
    "/refresh",
    response_model=TokenPair,
)
async def refresh_token(
    payload: RefreshRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Обновление JWT токенов.
    """

    service = AuthService(db)

    result = await service.refresh(
        payload.refresh_token,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    return result


@router.post("/logout")
async def logout(
    payload: RefreshRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Logout пользователя.
    """

    service = AuthService(db)

    await service.logout(
        payload.refresh_token,
    )

    return {
        "message": "Logged out successfully",
    }


@router.get("/health")
async def auth_health():
    """
    Проверка работы auth сервиса.
    """

    return {
        "status": "ok",
        "service": "auth",
    }