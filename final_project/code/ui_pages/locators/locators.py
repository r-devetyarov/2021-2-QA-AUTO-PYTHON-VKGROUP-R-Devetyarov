from selenium.webdriver.common.by import By


class LoginPageLocators:
    FIELD_INPUT_LOGIN = (By.NAME, 'username')
    FIELD_INPUT_PASSWORD = (By.NAME, 'password')
    LOGIN_BUTTON = (By.ID, 'submit')
    FAIL_LOGIN = (By.ID, 'flash')
    CREATE_ACCOUNT_BUTTON = (By.XPATH, '//a[@href="/reg"]')


class RegistrationPageLocators:
    FIELD_INPUT_USERNAME = (By.ID, 'username')
    # от 6 символов
    FIELD_INPUT_EMAIL = (By.ID, "email")
    FIELD_INPUT_PASSWORD = (By.ID, "password")
    FIELD_CONFIRM_PASSWORD = (By.ID, "confirm")
    CHECKBOX_ACCEPT = (By.ID, "term")
    REGISTER_BUTTON = (By.ID, "submit")
    INCORRECT_ALERT = (By.ID, "flash")


class MainPageLocators:
    LOGOUT_BUTTON = (By.ID, "logout")
    CURRENT_USER_TEXT = (By.XPATH, '//*[@id="login-name"]')
    WHAT_IS_API_BTN = (By.XPATH, '//a[@href="https://en.wikipedia.org/wiki/Application_programming_interface"]')
    FUTURE_OF_INTERNET_BTN = (
        By.XPATH,
        '//a[@href="https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/"]'
    )
    LETS_ABOUT_SMTP_BTN = (By.XPATH, '//a[@href="https://ru.wikipedia.org/wiki/SMTP"]')
    HOME_BUTTON = (By.XPATH, '//a[@href="/" and text()="HOME"]')
    PYTHON_BUTTON = (By.XPATH, '//a[@href="https://www.python.org/"]')
    PYTHON_HISTORY_BTN = (By.XPATH, '//a[@href="https://en.wikipedia.org/wiki/History_of_Python"]')
    PYTHON_FLASK_BTN = (By.XPATH, '//a[@href="https://flask.palletsprojects.com/en/1.1.x/#"]')
    LINUX_BUTTON = (By.XPATH, '//a[@href="javascript:" and text()="Linux"]')
    DOWNLOAD_CENTOS_BTN = (By.XPATH, '//a[@href="https://getfedora.org/ru/workstation/download/"]')
    NETWORK_BUTTON = (By.XPATH, '//a[@href="javascript:" and text()="Network"]')
    WIRESHARK_NEWS_BUTTON = (By.XPATH, '//a[@href="https://www.wireshark.org/news/"]')
    WIRESHARK_DOWNLOAD_BUTTON = (By.XPATH, '//a[@href="https://www.wireshark.org/#download"]')
    TCPDUMP_EXAMPLES_BTN = (By.XPATH, '//a[@href="https://hackertarget.com/tcpdump-examples/"]')
