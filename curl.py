from imp import new_module
# А - требуется токен Bearer

main_site = 'https://stellarburgers.nomoreparties.site/' # главная
register_api = main_site + 'api/auth/register' # создание нового пользователя

login_api = main_site + 'api/auth/login' # авторизация зарегистрированного пользователя А
user_api = main_site + 'api/auth/user' # получить, обновить, удалить данные о пользователе А

logout_api = main_site  + 'api/auth/logout' # выход из лк А
token_api = main_site + 'api/auth/token' # обновление токена
password_reset_api = main_site + 'api/password-reset' # восстановление пароля
reset_password_reset_api = main_site + 'api/password-reset/reset' # смена пароля

orders_api = main_site + 'api/orders' # заказы пользователя, создание заказа А
orders_all_api = main_site + 'api/orders/all' # список всех заказов
ingredients_api = main_site + 'api/ingredients' # получить список ингредиентов
