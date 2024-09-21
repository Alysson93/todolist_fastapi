from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from database import Session, get_session
from models import Todo
from schemas import TodoRequest, TodoResponse
from security import get_current_user

T_SESSION = Annotated[Session, Depends(get_session)]
T_USER = Annotated[Todo, Depends(get_current_user)]


router = APIRouter(prefix='/todos', tags=['todos'])

@router.post('/', response_model=TodoResponse, status_code=HTTPStatus.CREATED)
def create_todo(session: T_SESSION, user: T_USER, todo: TodoRequest):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo
