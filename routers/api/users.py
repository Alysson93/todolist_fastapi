from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from database import Session, get_session
from models import User
from schemas import UserRequest, UserResponse
from security import get_current_user, get_password_hash

T_SESSION = Annotated[Session, Depends(get_session)]
T_USER = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserResponse)
def create_user(user: UserRequest, session: T_SESSION):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='username or email already used by other user.',
        )
    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get('/', response_model=list[UserResponse])
def read_users(session: T_SESSION, skip: int = 0, limit: int = 100):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return users


@router.put('/{id}', status_code=HTTPStatus.NO_CONTENT)
def update_user(
    session: T_SESSION, current_user: T_USER, id: int, user: UserRequest
):
    if current_user.id != id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    db_user = session.scalar(select(User).where(User.id == id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    db_user.username = user.username
    db_user.password = get_password_hash(user.password)
    db_user.email = user.email
    session.commit()
    session.refresh(db_user)


@router.delete('/{id}', status_code=HTTPStatus.NO_CONTENT)
def delete_user(session: T_SESSION, user: T_USER, id: int):
    if user.id != id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    db_user = session.scalar(select(User).where(User.id == id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    session.delete(db_user)
    session.commit()
