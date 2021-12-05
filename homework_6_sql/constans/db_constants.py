import enum


class TablesName(str, enum.Enum):
    LINE_COUNT = 'line_count'
    METHOD_COUNT = 'methods_count'
    MOST_COMMON_URL = 'most_common_url'
    BAR_REQUEST_TOP_MAX_SIZE = 'bad_request_top_max_size'
    SERVER_ERROR_TOP_IP = 'server_error_top_ip'


class DbProperty(enum.Enum):
    DB_NAME = 'TEST_SQL'
    DB_HOST = '127.0.0.1'
    DB_PORT = 3306
    DB_USER_ROOT = 'root'
    DB_PASSWORD_ROOT = 'pass'

