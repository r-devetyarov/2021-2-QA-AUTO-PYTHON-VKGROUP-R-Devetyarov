from selenium.webdriver.common.by import By


class BasePageLocators:
    MY_EMAIL_BUTTON = (By.XPATH, "//div[contains(@class, 'right-module-rightButton')]")
    LOGOUT_BUTTON = (By.XPATH, "//a[@href='/logout']")
    SEGMENTS_BUTTON = (By.XPATH, "//a[@href='/segments']")
    BALANCE_BUTTON = (By.XPATH, "//a[@href='/billing']")
    STATISTICS_BUTTON = (By.XPATH, "//a[@href='/statistics']")
    PROFILE_BUTTON = (By.XPATH, "//a[@href='/profile']")


class LoginPageLocators(BasePageLocators):
    TO_COME_BUTTON = (By.XPATH, "//div[contains(@class, 'responseHead-module-button')]")
    FIELD_INPUT_LOGIN = (By.NAME, "email")
    FIELD_INPUT_PASSWORD = (By.NAME, "password")
    LOGIN_BUTTON_LP = (By.XPATH, '//div[contains(@class, "authForm-module-button")]')


class ProfilePageLocators(BasePageLocators):
    SEND_FIO = (By.XPATH, "//div[@data-name='fio']//input")
    GET_FIO = (By.XPATH, "//div[contains(@class, 'right-module-userNameWrap')]")
    SAVE_BUTTON = (By.XPATH, "//button[@data-class-name='Submit']")
