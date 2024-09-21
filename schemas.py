from pydantic import BaseModel, ConfigDict, EmailStr
from models import TodoState

class UserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class TodoRequest(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoResponse(TodoRequest):
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
