import allure
import pytest

from tests.tests_api.base import BaseCase
from utils import utils


@pytest.mark.API
@pytest.mark.ALL
@allure.feature("API tests")
@allure.story("Tests register user")
class TestApiRegister(BaseCase):

    @allure.title("Registry user with valid data")
    @pytest.mark.parametrize("username_len", [6, 8, 16])
    @pytest.mark.parametrize("password_len", [1, 34, 254, 255])
    @pytest.mark.parametrize("email_len", [6, 7, 33, 63, 64])
    def test_register_valid_data(self, username_len, password_len, email_len):
        username = utils.random_string(size=username_len)
        password = utils.random_string(size=password_len)
        email = utils.random_email(size=email_len)
        resp = self.api_client.add_user(username=username, password=password, email=email)
        # TODO bug: not correct response status code
        # assert resp.status_code == 201
        assert all(self.mysql.check_user_in_db(username=username, email=email, password=password))
        assert resp.text == "User was added!"

    @allure.title("Registry user with duplicate username")
    def test_register_duplicate_username(self):
        user_data = self.api_client.builder.user_data()
        self.api_client.add_user(
            username=user_data.username,
            password=user_data.password,
            email=user_data.email
        )

        new_user_data = self.api_client.builder.user_data()
        resp = self.api_client.add_user(
            username=user_data.username,
            password=user_data.password,
            email=new_user_data.email
        )
        assert resp.status_code == 304
        assert all(self.mysql.check_user_in_db(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
        ))

    @allure.title("Registry user with duplicate username")
    def test_register_duplicate_email(self):
        user_data = self.api_client.builder.user_data()
        self.api_client.add_user(
            username=user_data.username,
            password=user_data.password,
            email=user_data.email
        )

        new_user_data = self.api_client.builder.user_data()
        resp = self.api_client.add_user(
            username=new_user_data.username,
            password=user_data.password,
            email=user_data.email
        )
        assert resp.status_code == 304
        assert all(self.mysql.check_user_in_db(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
        ))

    @allure.title("Registry user without obligatory field")
    @pytest.mark.parametrize(
        "fields",
        [
            ("username", "password"),
            ("username", "email"),
            ("username",),
            ("password", "email"),
            ("password",),
            ("email",),
            ()

        ]
    )
    def test_register_without_obligatory_field(self, fields):
        user_data = self.api_client.builder.user_data()
        payload: dict = {}
        for filed in fields:
            if filed == "username":
                payload["username"] = user_data.username
            if filed == "password":
                payload["password"] = user_data.password
            if filed == "email":
                payload["email"] = user_data.email

        resp = self.api_client.add_user(request_data=payload)
        assert resp.status_code == 400

    @allure.title("Registry user with extra filed")
    def test_reqsit_with_extra_filed(self):
        field = utils.random_string()
        value = utils.random_string()
        user_data = self.api_client.builder.user_data()
        payload = {
            "username": user_data.username,
            "password": user_data.password,
            "email": user_data.email,
            field: value
        }
        resp = self.api_client.add_user(request_data=payload)
        assert all(self.mysql.check_user_in_db(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
        ))
        # assert resp.status_code == 201

    @allure.title("Registry user with invalid username length")
    @pytest.mark.parametrize("username_len", [0, 1, 5, 17, 445])
    def test_invalid_username_len(self, username_len):
        username = utils.random_string(size=username_len)
        resp = self.api_client.add_user(username=username)

        assert not all(self.mysql.check_user_in_db(username=username))
        assert resp.status_code == 400

    @allure.title("Registry user with invalid email length")
    @pytest.mark.parametrize("email_len", [0, 65, 321])
    def test_invalid_email_len(self, email_len):
        email = utils.random_email(size=email_len)
        user_data = self.api_client.builder.user_data()
        resp = self.api_client.add_user(email=email, username=user_data.username)

        assert not all(self.mysql.check_user_in_db(username=user_data.username))
        assert resp.status_code == 400

    @allure.title("Registry user with invalid password length")
    @pytest.mark.parametrize("password_len", [0, 256, 999])
    def test_invalid_password_len(self, password_len):
        password = utils.random_string(size=password_len)
        user_data = self.api_client.builder.user_data()
        resp = self.api_client.add_user(password=password, username=user_data.username)

        assert not all(self.mysql.check_user_in_db(
            username=user_data.username,
        ))
        assert resp.status_code == 400

    @allure.title("Test registration invalid email")
    @pytest.mark.parametrize("email_len", [0, 10])
    def test_invalid_email(self, email_len):
        user_data = self.api_client.builder.user_data()
        email = utils.random_string(size=email_len)
        resp = self.api_client.add_user(username=user_data.username, email=email)

        assert not all(self.mysql.check_user_in_db(username=user_data.username))
        assert resp.status_code == 400


@pytest.mark.API
@pytest.mark.ALL
@allure.feature("API tests")
@allure.story("Tests delete user")
class TestApiDeleteUser(BaseCase):

    @allure.title("Test delete created user")
    def test_delete_created_user(self, create_user):
        resp = self.api_client.delete_user(username=create_user.username)
        assert resp.status_code == 204
        assert not all(self.mysql.check_user_in_db(username=create_user.username))

    @allure.title("Test delete not created user")
    def test_delete_created_not_crated_user(self):
        username = utils.random_string()
        resp = self.api_client.delete_user(username=username)
        assert resp.status_code == 404


@pytest.mark.API
@pytest.mark.ALL
@allure.feature("API tests")
@allure.story("Tests block user")
class TestApiBlockUser(BaseCase):

    @allure.title("Test block created user")
    def test_block_created_user(self, create_user):
        resp = self.api_client.block_user(username=create_user.username)
        assert resp.status_code == 200
        assert all(self.mysql.check_user_in_db(username=create_user.username, access=0))

        resp = self.api_client.login(username=create_user.username, password=create_user.password, set_session=False)
        assert resp.status_code == 401

    @allure.title("Test block not created user")
    def test_block_not_created_user(self):
        username = utils.random_string()
        resp = self.api_client.block_user(username=username)
        assert resp.status_code == 404

    @allure.title("Test block blocked user")
    def test_block_blocked_user(self):
        create_user = self.mysql.add_user(access=0)
        resp = self.api_client.block_user(username=create_user.username)
        assert resp.status_code == 304
        assert all(self.mysql.check_user_in_db(username=create_user.username, access=0))

        resp = self.api_client.login(username=create_user.username, password=create_user.password, set_session=False)
        assert resp.status_code == 401


@pytest.mark.API
@pytest.mark.ALL
@allure.feature("API tests")
@allure.story("Tests accept user")
class TestApiAcceptUser(BaseCase):

    @allure.title("Test accept accepted created user")
    def test_accept_accepted_created_user(self, create_user):
        resp = self.api_client.access_user(username=create_user.username)
        assert resp.status_code == 304
        assert all(self.mysql.check_user_in_db(username=create_user.username, access=1))

        resp = self.api_client.login(username=create_user.username, password=create_user.password, set_session=False)
        assert resp.status_code == 200

    @allure.title("Test accept not created user")
    def test_access_not_created_user(self):
        username = utils.random_string()
        resp = self.api_client.access_user(username=username)
        assert resp.status_code == 404

    @allure.title("Test accept blocked user")
    def test_access_blocked_user(self):
        create_user = self.mysql.add_user(access=0)
        resp = self.api_client.access_user(username=create_user.username)
        assert resp.status_code == 200
        assert all(self.mysql.check_user_in_db(username=create_user.username, access=1))

        resp = self.api_client.login(username=create_user.username, password=create_user.password, set_session=False)
        assert resp.status_code == 200


@pytest.mark.API
@pytest.mark.ALL
@allure.feature("API tests")
@allure.story("Tests get status app")
class TestApiGetStatusApp(BaseCase):

    @allure.step("Test get status running app")
    def test_get_status_running_app(self):
        resp = self.api_client.get_status_app()
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}


@pytest.mark.API
@pytest.mark.ALL
@allure.feature("API tests")
@allure.story("Tests without authorized")
class TestApiWithoutAuth(BaseCase):
    authorized = False

    @allure.step("Test add user without authorized")
    def test_add_user_without_auth(self):
        resp = self.api_client.add_user()
        assert resp.status_code == 401

    @allure.step("Test delete user without authorized")
    def test_delete_user_without_auth(self):
        resp = self.api_client.delete_user(username=utils.random_string())
        assert resp.status_code == 401

    @allure.step("Test block user without authorized")
    def test_block_user_without_auth(self):
        resp = self.api_client.block_user(username=utils.random_string())
        assert resp.status_code == 401

    @allure.step("Test access user without authorized")
    def test_access_user_without_auth(self):
        resp = self.api_client.access_user(username=utils.random_string())
        assert resp.status_code == 401
