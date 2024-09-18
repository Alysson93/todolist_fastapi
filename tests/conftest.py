import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')

from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from database import get_session
from main import app
from models import User, table_registry
from security import get_password_hash


@fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client
    app.dependency_overrides.clear()


@fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    table_registry.metadata.drop_all(engine)


@fixture
def user(session):
    user = User(
        username='John Doe',
        email='john@mail.com',
        password=get_password_hash('123'),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@fixture
def token(client, user):
    response = client.post(
        '/api/auth/token', data={'username': user.username, 'password': '123'}
    )
    return response.json()['access_token']
