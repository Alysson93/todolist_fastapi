from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select

from database import Session, get_session
from models import User
from schemas import TokenData
from settings import Settings

pwd_context = PasswordHash.recommended()
oauth2 = OAuth2PasswordBearer(tokenUrl='api/auth/token')


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        to_encode, Settings().SECRET_KEY, algorithm=Settings().ALGORITHM
    )
    return encoded_jwt


def get_current_user(
    session: Session = Depends(get_session), token: str = Depends(oauth2)
):
    credential_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = decode(
            token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM]
        )
        username: str = payload.get('sub')
        if not username:
            raise credential_exception
        token_data = TokenData(username=username)
    except DecodeError:
        raise credential_exception
    user = session.scalar(select(User).where(User.username == username))
    if not user:
        raise credential_exception
    return user
