from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        '/api/auth/token', data={'username': user.username, 'password': '123'}
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token
