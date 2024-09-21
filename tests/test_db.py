from sqlalchemy import select

from models import User, Todo


def test_create_user(session):
    new_user = User(username='John Doe', email='john@mail.com', password='123')
    session.add(new_user)
    session.commit()
    user = session.scalar(select(User).where(User.username == 'John Doe'))
    assert user.username == 'John Doe'


def test_create_todo(session, user):
    todo = Todo(title='Estudar Python', description='Web e automações', state='draft', user_id=user.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    user = session.scalar(select(User).where(User.username == user.username))
    assert todo in user.todos