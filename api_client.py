import requests
import json
import allure
import curl
import time

class APIClient:
    def __init__(self, base_url=curl.main_site):
        self.base_url = base_url
        self.headers = {'Content-Type': 'application/json'}

    def _get_headers_with_token(self, token):
        """Вспомогательная функция для добавления токена в заголовок Authorization."""
        headers = self.headers.copy()  # Создаем копию основных заголовков
        if token:
            headers['Authorization'] = f"{token}"
        return headers

    @allure.step("Регистрация пользователя")
    def register_user(self, email, password, name):
        url = curl.register_api
        payload = {"email": email, "password": password, "name": name}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        return response

    @allure.step("Авторизация пользователя")
    def login_user(self, email, password):
        url = curl.login_api
        payload = {"email": email, "password": password}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        return response

    @allure.step("Выход пользователя из системы")
    def logout_user(self, refresh_token):
        url = curl.logout_api
        payload = {"token": refresh_token}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        return response

    @allure.step("Обновление токена")
    def refresh_token(self, refresh_token):
        url = curl.token_api
        payload = {"token": refresh_token}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        return response

    @allure.step("Изменение данных пользователя") #
    def update_user(self, token, **kwargs): #=None, email=None, password=None):
        url = curl.user_api
        headers = self._get_headers_with_token(token)  # Получаем заголовки с токеном
        response = requests.patch(url, data=json.dumps(kwargs), headers=headers)
        return response

    @allure.step("Инициация сброса пароля")
    def reset_password_request(self, email):
        url = curl.password_reset_api
        payload = {"email": email}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        return response

    @allure.step("Сброс пароля")
    def reset_password_confirm(self, password, token):
        url = curl.reset_password_reset_api
        payload = {"password": password, "token": token}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        return response

    @allure.step("Получение списка ингредиентов")
    def get_ingredients(self):
        url = curl.ingredients_api
        response = requests.get(url, headers=self.headers)
        return response

    @allure.step("Создание заказа")
    def create_order(self, ingredients, token=None):
        url = curl.orders_api
        # Token по умолчанию None
        payload = {"ingredients": ingredients}
        headers = self._get_headers_with_token(token)  # Получаем заголовки с токеном
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return response

    @allure.step("Получение заказов пользователя")
    def get_user_orders(self, token=None):
        url = curl.orders_api
        headers = self._get_headers_with_token(token)  # Получаем заголовки с токеном
        response = requests.get(url, headers=headers)
        return response

    @allure.step("Получение всех заказов (для socket-соединения)")
    def get_all_orders(self, token=None):#Установим значение токена по умолчанию в None
        url = curl.orders_all_api
        headers = self._get_headers_with_token(token)  # Получаем заголовки с токеном
        response = requests.get(url, headers=headers)
        return response

    @allure.step("Удаление пользователя")
    def delete_user(self, token):
         print(f"Deleting user with token: {token}")  # Добавили print
         url = curl.user_api
         headers = self._get_headers_with_token(token)  # Добавляем токен в заголовок
         response = requests.delete(url, headers=headers)
         print(f"Delete user response status code: {response.status_code}, json: {response.json()}")  # Добавили print
         time.sleep(0.1)
         return response
