class TestData:
    """Все ответы API"""

    """создание пользователя """
    CREATE_USER_WITHOUT_DATA = "Email, password and name are required fields"  # 403
    CREATE_USER_ALREADY_EXISTS = "User already exists"  # 403

    """логин пользователя """
    BAD_LOGIN = "email or password are incorrect"

    """ изменение данных пользователя """
    CHANGE_USER_DATA = "You should be authorised" #

    EMAIL_DUPLICATE = "User with such email already exists"

    """ создание заказа """
    CREATE_ORDER_WITHOUT_INGRED = "Ingredient ids must be provided"  # 400

    """получение заказов конкретного пользователя """
    GET_ORDER_USER_ANAUTORIZ = "You should be authorised"  # 401




