import pytest
from api_client import APIClient
from data import TestData
import secrets
import string
import allure

@pytest.fixture(scope="function")
def api_client():
    """Фикстура для создания экземпляра ApiClient, чтобы не прописывать в каждом тесте"""
    return APIClient(curl.main_site)

@pytest.fixture(scope="function")
def new_user_data(api_client):
    """Фикстура для создания случайных данных пользователя: почта, пароль, имя"""
    email = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(10)) + "@example.com"
    password = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(10))
    name = "Test User1"
    return {"email": email, "password": password, "name": name}

@pytest.fixture()
def registered_user(api_client, new_user_data):
    """Фикстура для регистрации пользователя."""
    register_response = api_client.register_user(
        new_user_data["email"],
        new_user_data["password"],
        new_user_data["name"])
    assert register_response.status_code == 200
    assert register_response.json()["success"] is True

    return {"email": new_user_data["email"], #Сохраняем email
            "password": new_user_data["password"], #Сохраняем пароль
            "name": new_user_data["name"], #Сохраняем имя
            "token": register_response.json()["accessToken"], #Сохраняем токен]
            "refresh_token": register_response.json()["refreshToken"]
            }


@pytest.fixture()
def logged_in_user(api_client, registered_user): #
    """Фикстура для авторизации пользователя."""
    login_response = api_client.login_user(registered_user["email"], registered_user["password"])
    print(f"Login response status: {login_response.status_code}, json: {login_response.json()}")  # Добавили print
    access_token = login_response.json().get('accessToken')
    refresh_token = login_response.json().get('refreshToken')
    print(f"Access token: {access_token}")  # Добавили print
    return {
        "email": registered_user["email"],
        "password": registered_user["password"],
        "name": registered_user["name"],
        "token": access_token,
        "refreshToken": refresh_token
    }

@pytest.fixture()
def delete_user(api_client, registered_user):
        """Фикстура для удаления пользователя."""
        print("delete_user: Fixture started")
        yield
        # Пытаемся залогиниться, чтобы получить токен для удаления
        try:
            login_response = api_client.login_user(registered_user["email"], registered_user["password"])
            if login_response.status_code == 200 and login_response.json()["success"]:
                token = login_response.json()["accessToken"]
                delete_response = api_client.delete_user(token)
                print(f"Delete response: {delete_response.status_code}, {delete_response.json()}")
            else:
                print("Не удалось залогиниться для удаления пользователя")
        except Exception as e:
            print(f"Ошибка при удалении пользователя: {e}")


# Добавляем фикстуру для обновления email - непонятно, нужна ли она вообще
@pytest.fixture()
def update_registered_user_data(api_client):
    """Фикстура для обновления данных пользователя."""
    def _update_registered_user_data(registered_user_data, field, value):
        token = registered_user_data["register_response"].json()["accessToken"]
        response = api_client.update_user(token, **{field: value})
        assert response.status_code == 200
        assert response.json()["success"] is True

        #Обновляем данные пользователя в фикстуре
        if field == "email":
            registered_user_data["email"] = value
        elif field == "name":
            registered_user_data["name"] = value
        return registered_user_data
    return _update_registered_user_data
