import hashlib

from sqlalchemy import select

from app.database.models.refresh_token import RefreshToken


class AuthRepository:

    def __init__(self, db):
        self.db = db

    @staticmethod
    def token_hash(token: str) -> str:
        return hashlib.sha256(
            token.encode()
        ).hexdigest()

    async def save_refresh_token(
        self,
        user_id: int,
        token: str,
        expires_at
    ):

        refresh = RefreshToken(
            user_id=user_id,
            token_hash=self.token_hash(token),
            expires_at=expires_at
        )

        self.db.add(refresh)

        await self.db.commit()

    async def get_refresh_token(
        self,
        token: str
    ):

        stmt = select(
            RefreshToken
        ).where(
            RefreshToken.token_hash ==
            self.token_hash(token)
        )

        result = await self.db.execute(
            stmt
        )

        return result.scalar_one_or_none()