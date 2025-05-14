import pytest
import allure
from data import TestData

@allure.feature("Заказы")
class TestOrders:
    @pytest.fixture(scope="function")
    def get_ingredients_hashes(self, api_client):
        """Получает список ингредиентов и возвращает их хеши."""
        response = api_client.get_ingredients()
        assert response.status_code == 200
        ingredients = response.json()['data']
        ingredient_hashes = [i['_id'] for i in ingredients]
        return ingredient_hashes


    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_authorized_with_ingredients(self, api_client, get_ingredients_hashes, logged_in_user):
        ingredients = get_ingredients_hashes[:3]
        response = api_client.create_order(ingredients, logged_in_user["token"])
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()
        assert "name" in response.json()
        assert "number" in response.json()["order"]

    @allure.title("Создание заказа без авторизации с ингредиентами")
    def test_create_order_unauthorized_with_ingredients(self, api_client, get_ingredients_hashes):
        ingredients = get_ingredients_hashes[:3]
        response = api_client.create_order(ingredients)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()
        assert "name" in response.json()
        assert "number" in response.json()["order"]

    @allure.title("Создание заказа с авторизацией без ингредиентов (ошибка)")
    def test_create_order_authorized_no_ingredients(self, api_client, logged_in_user):
        response = api_client.create_order([], logged_in_user["token"])
        assert response.status_code == 400
        assert response.json()["success"] is False
        assert response.json()["message"] == TestData.CREATE_ORDER_WITHOUT_INGRED

    @allure.title("Создание заказа без авторизации и без ингредиентов (ошибка)")
    def test_create_order_unauthorized_no_ingredients(self, api_client):
        response = api_client.create_order([])
        assert response.status_code == 400
        assert response.json()["success"] is False
        assert response.json()["message"] == TestData.CREATE_ORDER_WITHOUT_INGRED

    @allure.title("Создание заказа с неверным хешем ингредиентов (ошибка)")
    def test_create_order_invalid_ingredient_hash(self, api_client, logged_in_user,get_ingredients_hashes):
        # Используем ингредиенты из списка, который уже получили в фикстуре
        valid_ingredients = get_ingredients_hashes
        # Получаем список всех ингридиентов
        response_get = api_client.get_ingredients()
        all_ingredients = [i['_id'] for i in response_get.json()['data']]
        # Добавляем в массив с валидными ингредиентами несуществующие
        invalid_ingredients = ["invalid_hash1", "invalid_hash2"]
        # Объединяем списки, передаем в метод
        invalid_ingredients_combined = valid_ingredients + invalid_ingredients
        response = api_client.create_order(invalid_ingredients_combined, logged_in_user["token"])
        assert response.status_code == 500

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_user_orders_authorized(self, api_client, logged_in_user):
        response = api_client.get_user_orders(logged_in_user["token"])
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "orders" in response.json()

    @allure.title("Получение заказов неавторизованного пользователя (ошибка)")
    def test_get_user_orders_unauthorized(self, api_client, logged_in_user):
        response = api_client.get_user_orders()
        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == TestData.GET_ORDER_USER_ANAUTORIZ

    @allure.title("Получение всех заказов с авторизацией (для socket-соединения)")# возможно этот тест нужно изменить или удалить
    def test_get_all_orders_authorized(self, api_client):
        response = api_client.get_all_orders()
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "orders" in response.json()
        assert "total" in response.json()
        assert "totalToday" in response.json()

    @allure.title("Получение всех заказов без авторизации (для socket-соединения, ожидаем 200)")
    def test_get_all_orders_unauthorized(self, api_client):
        response = api_client.get_all_orders()
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "orders" in response.json()
        assert "total" in response.json()
        assert "totalToday" in response.json()
