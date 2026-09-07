from datetime import datetime, timedelta, timezone

import jwt
from app.config import JWT_SECRET_KEY
from exceptions.security_exceptions import InvalidAccessTokenError

ALGORITHM = "HS256"


def create_access_token(user_id: str) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(minutes=30)

    payload = {
        "sub": user_id,
        "exp": expiration,
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except jwt.InvalidTokenError as error:
        raise InvalidAccessTokenError("Access token is invalid") from error
