from jwt import decode

from security import create_access_token
from settings import Settings


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)
    decoded = decode(
        token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM]
    )
    assert decoded['test'] == data['test']
    assert decoded['exp']
