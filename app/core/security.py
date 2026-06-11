from datetime import datetime, timedelta, UTC
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


# ============================================================
# PASSWORD HASHING
# ============================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)


def hash_password(password):


    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify password.
    """

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ============================================================
# JWT TOKENS
# ============================================================

def create_access_token(
    data: dict[str, Any]
) -> str:
    """
    Create access token.
    """

    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {
            "exp": expire,
            "type": "access"
        }
    )

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def create_refresh_token(
    data: dict[str, Any]
) -> str:
    """
    Create refresh token.
    """

    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    to_encode.update(
        {
            "exp": expire,
            "type": "refresh"
        }
    )

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


# ============================================================
# TOKEN DECODING
# ============================================================

def decode_token(
    token: str
) -> dict[str, Any]:
    """
    Decode JWT token.
    """

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        return payload

    except JWTError as exc:
        raise ValueError(
            "Invalid token"
        ) from exc


def verify_access_token(
    token: str
) -> dict[str, Any]:
    """
    Verify access token.
    """

    payload = decode_token(token)

    token_type = payload.get("type")

    if token_type != "access":
        raise ValueError(
            "Invalid access token"
        )

    return payload


def verify_refresh_token(
    token: str
) -> dict[str, Any]:
    """
    Verify refresh token.
    """

    payload = decode_token(token)

    token_type = payload.get("type")

    if token_type != "refresh":
        raise ValueError(
            "Invalid refresh token"
        )

    return payload


# ============================================================
# USER HELPERS
# ============================================================

def get_user_id_from_token(
    token: str
) -> int:
    """
    Extract user id from token.
    """

    payload = verify_access_token(token)

    user_id = payload.get("sub")

    if user_id is None:
        raise ValueError(
            "User ID missing in token"
        )

    return int(user_id)


def get_email_from_token(
    token: str
) -> str:
    """
    Extract email from token.
    """

    payload = verify_access_token(token)

    email = payload.get("email")

    if not email:
        raise ValueError(
            "Email missing in token"
        )

    return email