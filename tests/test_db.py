from sqlalchemy import select

from models import User


def test_create_user(session):
    new_user = User(username='John Doe', email='john@mail.com', password='123')
    session.add(new_user)
    session.commit()
    user = session.scalar(select(User).where(User.username == 'John Doe'))
    assert user.username == 'John Doe'
