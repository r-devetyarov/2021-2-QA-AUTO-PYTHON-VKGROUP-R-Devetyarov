import enum


class AppConstants:
    HOST = "application"
    APP_PORT = 8079
    BASE_URL = f"http://{HOST}:{APP_PORT}"


class ProxyAppConstants:
    HOST = "myapp_proxy"
    APP_PORT = 8070
    BASE_URL = f"http://{HOST}:{APP_PORT}"


class MockConstants:
    HOST = "vk_mock"
    MOCK_PORT = 5000
    MOCK_URL = f"http://{HOST}:{MOCK_PORT}"


class DefaultUser:
    USERNAME = "administrator"
    PASSWORD = "admin123"
    EMAIL = "admin_email@email.com"


class DbProperty:
    HOST = "percona"
    DB_NAME = "TEST"
    DB_PORT = 3306
    DB_USER = "test_qa"
    DB_PASS = "qa_test"


class TablesName(str, enum.Enum):
    TEST_USERS = "test_users"
