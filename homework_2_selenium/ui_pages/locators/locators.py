from selenium.webdriver.common.by import By


class BasePageLocators:
    MY_EMAIL_BUTTON = (By.XPATH, "//div[contains(@class, 'right-module-rightButton')]")
    LOGOUT_BUTTON = (By.XPATH, "//a[@href='/logout']")
    SEGMENTS_BUTTON = (By.XPATH, "//a[@href='/segments']")
    BALANCE_BUTTON = (By.XPATH, "//a[@href='/billing']")
    STATISTICS_BUTTON = (By.XPATH, "//a[@href='/statistics']")
    PROFILE_BUTTON = (By.XPATH, "//a[@href='/profile']")
    COMPANY_BUTTON = (By.XPATH, "//a[@href='/dashboard']")
    FORGOT_PASSWORD = (By.XPATH, '//*[@class="pull-left ext-forgotPasswdLink"]')


class LoginPageLocators(BasePageLocators):
    TO_COME_BUTTON = (By.XPATH, "//div[contains(@class, 'responseHead-module-button')]")
    FIELD_INPUT_LOGIN = (By.NAME, "email")
    FIELD_INPUT_PASSWORD = (By.NAME, "password")
    LOGIN_BUTTON_LP = (By.XPATH, '//div[contains(@class, "authForm-module-button")]')


class ProfilePageLocators(BasePageLocators):
    SEND_FIO = (By.XPATH, "//div[@data-name='fio']//input")
    GET_FIO = (By.XPATH, "//div[contains(@class, 'right-module-userNameWrap')]")
    SAVE_BUTTON = (By.XPATH, "//button[@data-class-name='Submit']")


class SegmentsPageLocators(BasePageLocators):
    __CLASS_SEGMENT_LIST = "//div[@class='segments-list']"
    CREATE_SEGMENT_FIRST = (By.XPATH, f"{__CLASS_SEGMENT_LIST}//*[@href='/segments/segments_list/new/']")
    CREATE_SEGMENT_NOT_FIRST = (By.XPATH, f"{__CLASS_SEGMENT_LIST}//button[@data-class-name='Submit']")
    CREATE_SEGMENT_NAME_FILED = (By.XPATH, '//div[@class="input input_create-segment-form"]//input')
    CREATE_ITEM_GAMES_SN = (By.XPATH, '//div[contains(@class, "adding-segments-modal__block-left")]/div[8]')
    CREATE_ITEMS_GAMES_CHECKBOX = (By.XPATH, "//input[contains(@class, 'adding-segments-source') and @type='checkbox']")
    BUTTON_SUBMIT = (By.XPATH, '//button[@class="button button_submit"]')
    ADD_SEGMENT_BUTTON = (
        By.XPATH, f'//div[contains(@class, "adding-segments-modal")]//button[@class="button button_submit"]')

    SEGMENT_ID = (By.XPATH, "//div[contains(@data-test, 'id-')]")
    CONFIRM_DELETE = (By.XPATH, "//button[contains(@class, 'confirm-remove')]")

    @staticmethod
    def segment_name_title(segment_name):
        return By.XPATH, f"//a[@title='{segment_name}']"

    @staticmethod
    def delete_segment_id_button(segment_id: str):
        return By.XPATH, f"//div[contains(@data-test, 'remove-{segment_id}')]"


class CompanyPageLocators(BasePageLocators):
    CREATE_COMPANY_NOT_FIRST = (By.XPATH, '//div[contains(@class,"dashboard-module-createButton")]/div')
    GOAL_TRAFFIC_BUTTON = (By.XPATH, '//div[contains(@class,"traffic")]')
    FIELD_INPUT_URL = (By.XPATH, '//input[contains(@class, "mainUrl") and @type="text"]')
    FIELD_INPUT_COMPANY_NAME = (By.XPATH, '//div[contains(@class, "campaign-name")]//input')
    COMPANY_ID = (By.XPATH, "//div[contains(@data-test, 'id-')]")
    DELETE_COMPANY_BUTTON = (By.XPATH, '//li[@data-test="3"]')

    @staticmethod
    def company_name_title(company_name):
        return By.XPATH, f"//a[@title='{company_name}']"

    @staticmethod
    def settings_company(company_id: str):
        return By.XPATH, f"//div[contains(@data-test, 'settings-{company_id}')]/div/input"

