from http import HTTPStatus

from schemas import UserResponse


def test_create_user(client):
    response = client.post(
        '/api/users',
        json={
            'username': 'John Doe',
            'email': 'john@mail.com',
            'password': '123',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'John Doe',
        'email': 'john@mail.com',
    }


def test_read_user(client, user):
    user_schema = UserResponse.model_validate(user).model_dump()
    response = client.get('/api/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [user_schema]


def test_read_users_empty(client):
    response = client.get('/api/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


def test_update_user(client, user, token):
    response = client.put(
        '/api/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Jane Doe',
            'email': 'jane@mail.com',
            'password': '456',
        },
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_update_user_not_found(client, token):
    response = client.put(
        '/api/users/2',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Jane Doe',
            'email': 'jane@mail.com',
            'password': '456',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_user(client, user, token):
    response = client.delete(
        '/api/users/1', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_user_not_found(client, token):
    response = client.delete(
        '/api/users/2', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
