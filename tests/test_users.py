from http import HTTPStatus

from fast_zero.schemas import UserPublic, UserSchema


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'teste',
            'password': '123456',
            'email': 'teste@intelbras.com.br',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'teste',
        'email': 'teste@intelbras.com.br',
        'id': 1,
    }


def test_read_users_without_user(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user, other_user):
    user_schema1 = UserPublic.model_validate(user).model_dump()
    user_schema2 = UserPublic.model_validate(other_user).model_dump()

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema1, user_schema2]}


def test_read_user_by_id(client, user):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': 1,
    }


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'otavio',
            'password': '123456',
            'email': 'otavio@intelbras.com.br',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'otavio',
        'email': 'otavio@intelbras.com.br',
        'id': user.id,
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.json() == {'message': 'User deleted'}


def test_not_found_read_user_by_id(client):
    response = client.get('/users/2')
    assert response.json() == {'detail': 'User not found'}


def test_delete_user_wrong_user(client, user, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_user_wrong_user(client, user, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'jeffim',
            'password': '654321',
            'email': 'jefim@mtgay.com.br',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_create_user_username_alredy_exists(client, user):
    user_schema = UserSchema.model_validate(user).model_dump()
    user_schema['email'] = 'username@already.exist'

    response = client.post('/users/', json=user_schema)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_alredy_exists(client, user):
    user_schema = UserSchema.model_validate(user).model_dump()
    user_schema['username'] = 'email already exists'

    response = client.post('/users/', json=user_schema)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}
