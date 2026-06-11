from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status

from app.database.models.user import User

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
)



class AuthService:

    def __init__(
        self,
        db: AsyncSession
    ):
        self.db = db

    async def get_user_by_email(
        self,
        email: str
    ) -> User | None:

        result = await self.db.execute(
            select(User).where(
                User.email == email
            )
        )

        return result.scalar_one_or_none()

    async def get_user_by_id(
        self,
        user_id: int
    ) -> User | None:

        result = await self.db.execute(
            select(User).where(
                User.id == user_id
            )
        )

        return result.scalar_one_or_none()

    async def register_user(
        self,
        email: str,
        password: str
    ) -> User:

        existing_user = await self.get_user_by_email(
            email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )

        user = User(
            email=email,
            password_hash=hash_password(
                password
            ),
            is_active=True,
            role="user"
        )

        self.db.add(user)

        await self.db.commit()

        await self.db.refresh(user)

        return user

    async def authenticate_user(
        self,
        email: str,
        password: str
    ) -> User:

        user = await self.get_user_by_email(
            email
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        if not verify_password(
            password,
            user.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is inactive"
            )

        return user

    async def login(
        self,
        email: str,
        password: str
    ):

        user = await self.authenticate_user(
            email,
            password
        )

        payload = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        }

        access_token = create_access_token(
            payload
        )

        refresh_token = create_refresh_token(
            payload
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    async def refresh(
        self,
        refresh_token: str
    ):

        try:

            payload = verify_refresh_token(
                refresh_token
            )

            user_id = int(
                payload["sub"]
            )

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        user = await self.get_user_by_id(
            user_id
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        new_payload = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        }

        return {
            "access_token": create_access_token(
                new_payload
            ),
            "refresh_token": create_refresh_token(
                new_payload
            ),
            "token_type": "bearer"
        }

    async def logout(
        self,
        refresh_token: str
    ):

        try:

            payload = verify_refresh_token(
                refresh_token
            )

            exp = payload.get(
                "exp"
            )



        except Exception:
            pass

        return True