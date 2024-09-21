from http import HTTPStatus

from schemas import TodoResponse


def test_create_todo(client, token):
    response = client.post(
        '/api/todos',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Estudar Python',
            'description': 'Web e automações',
            'state': 'draft',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'title': 'Estudar Python',
        'description': 'Web e automações',
        'state': 'draft'
    }