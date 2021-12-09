import enum


class AppConstants:
    HOST = "127.0.0.1"
    APP_PORT = 8079
    BASE_URL = f"http://{HOST}:{APP_PORT}"


class DefaultUser:
    USERNAME = "administrator"
    PASSWORD = "administrator"
    EMAIL = "admin_email@email.com"


class DbProperty(AppConstants):
    DB_NAME = "TEST"
    DB_PORT = 3306
    DB_USER = "test_qa"
    DB_PASS = "qa_test"


class TablesName(str, enum.Enum):
    TEST_USERS = "test_users"
