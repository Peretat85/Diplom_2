import pytest
import allure
from data import TestData

@allure.feature("Аутентификация")
class TestUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, api_client, new_user_data, delete_user): # передаем аргументы для создания и уделяем после теста
        # тест проходит, проверка осуществляется через возможности зайти под созданным пользователем, как в 7 спринте
        register_response = api_client.login_user(
            new_user_data['email'],
            new_user_data['password']
        )
        assert register_response.status_code == 200
        assert register_response.json()["success"] is True
        assert "accessToken" in register_response.json()
        assert "refreshToken" in register_response.json()
        assert "user" in register_response.json()
        assert "email" in register_response.json()["user"]
        assert "name" in register_response.json()["user"]


    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, api_client, new_user_data, registered_user, delete_user):
        response = api_client.register_user(
            registered_user['email'],
            registered_user['password'],
            registered_user['name']
        )

        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == TestData.CREATE_USER_ALREADY_EXISTS

    @allure.title("Создание пользователя без обязательных полей")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, api_client, missing_field):
        email = "test@example.com" if missing_field != "email" else None
        password = "password123" if missing_field != "password" else None
        name = "Test User" if missing_field != "name" else None

        response = api_client.register_user(email, password, name)
        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == TestData.CREATE_USER_WITHOUT_DATA

    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user(self, api_client, new_user_data, registered_user):
        response = api_client.login_user(
            new_user_data['email'],
            new_user_data['password']
        )
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()
        assert "refreshToken" in response.json()
        assert "user" in response.json()
        assert "email" in response.json()["user"]
        assert "name" in response.json()["user"]

    @allure.title("Логин с неверным логином и паролем") # проверить нужен ли токен в ручке?
    def test_login_invalid_credentials(self, api_client):
        response = api_client.login_user("invalid@example.com", "wrongpassword")
        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == TestData.BAD_LOGIN

@allure.feature("Обновление данных пользователя")
class TestUserUpdate:
    @allure.title("Изменение данных пользователя с авторизацией")
    @allure.title("Изменение имени пользователя")
    def test_update_user_name_authorized(self, api_client, registered_user, delete_user):
        new_name = "New Name"
        token = registered_user["token"] # получаем токен нового пользователя
        response = api_client.update_user(token, name=new_name)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["user"]["name"] == new_name

    @allure.title("Изменение email пользователя")
    def test_update_user_email_authorized(self, api_client, registered_user, delete_user):
        new_email = "ne213wemail@example.com"
        token = registered_user["token"]
        response = api_client.update_user(token, email=new_email)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["user"]["email"] == new_email



    @allure.title("Изменение email пользователя на уже существующий")
    def test_update_user_email_duplicate(self, api_client, registered_user, new_user_data, delete_user):
        # 1. регистрируем первого пользователя (без фикстуры)
        register_response_2 = api_client.register_user(new_user_data["email"], new_user_data["password"],
                                                       new_user_data["name"])

        new_email = register_response_2["email"]

        # 2. меняем второму пользователю почту на почту первого пользователя

        token = registered_user["token"]
        response = api_client.update_user(token, email=new_user_data["email"])

        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == TestData.EMAIL_DUPLICATE

    @allure.title("Изменение данных пользователя без авторизации")
    def test_update_user_unauthorized(self, api_client, new_user_data):
        # token = logged_in_user["token"]  # Получаем токен из logged_in_user
        token = ""  # Токен не передаем

        response = api_client.update_user(token, name="Some Name")

        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == TestData.CHANGE_USER_DATA
