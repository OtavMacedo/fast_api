from http import HTTPStatus

from fast_zero.schemas import UserPublic, UserSchema


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # act

    assert response.status_code == HTTPStatus.OK  # assert
    assert response.json() == {'message': 'ola mundo'}


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


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user_by_id(client, user):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'UserTeste',
        'email': 'teste@teste.com',
        'id': 1,
    }


def test_update_user(client, user):
    response = client.put(
        '/users/1',
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
        'id': 1,
    }


def test_delete_user(client, user):
    response = client.delete('/users/1')
    assert response.json() == {'message': 'User deleted'}


def test_not_found_delete_user(client):
    response = client.delete(
        '/users/2',
    )
    assert response.json() == {'detail': 'User not found'}


def test_not_found_read_user_by_id(client):
    response = client.get('/users/2')
    assert response.json() == {'detail': 'User not found'}


def test_not_found_update_user(client):
    response = client.put(
        '/users/2',
        json={
            'username': 'jeffim',
            'password': '654321',
            'email': 'jefim@mtgay.com.br',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_create_user_username_alredy_exists(client, user):
    user_schema = UserSchema.model_validate(user).model_dump()
    user_schema['email'] = 'username@already.exist'

    response = client.post(
        '/users/',
        json=user_schema
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_alredy_exists(client, user):
    user_schema = UserSchema.model_validate(user).model_dump()
    user_schema['username'] = 'email already exists'

    response = client.post(
        '/users/',
        json=user_schema
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}
