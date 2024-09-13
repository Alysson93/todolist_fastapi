from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from database import Session, get_session
from models import User
from schemas import Token
from security import create_access_token, verify_password

T_SESSION = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token', response_model=Token)
def login_for_token(
    session: T_SESSION, form_data: OAuth2PasswordRequestForm = Depends()
):
    user = session.scalar(
        select(User).where(User.username == form_data.username)
    )
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect username or password',
        )
    access_token = create_access_token(data={'sub': user.username})
    return {'access_token': access_token, 'token_type': 'bearer'}
