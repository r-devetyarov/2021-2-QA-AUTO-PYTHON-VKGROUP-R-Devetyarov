from uuid import uuid4

import pytest
from faker import Faker

import settings
from mock.flask_mock import USER_DATA

url = f'http://{settings.APP_HOST}:{settings.APP_PORT}'


class BaseCase:

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, api, logger):
        self.api = api
        self.logger = logger
        self.faker: Faker = Faker()

    def delete_user(self, user_id, expected_status=200):
        return self.api.send_request(method="DELETE", path=f"/delete_user/{user_id}", expected_status=expected_status)

    def change_user(self, payload: dict, expected_status=200):
        return self.api.send_request(method="PUT", path="/change_user", expected_status=expected_status, json=payload)

    def generate_user(self) -> dict:
        data = tuple(self.faker.name().split(' '))
        name, surname = data[0], data[1]
        return {"id": str(uuid4()), "name": name, "surname": surname}

    @staticmethod
    def send_user_in_mock(user_data: dict):
        USER_DATA.update({user_data["id"]: {"name": user_data['name'], "surname": user_data['surname']}})


class TestMockDeleteUser(BaseCase):
    def test_delete_exist_user(self):
        user_id = str(uuid4())
        USER_DATA[str(user_id)] = "my_user"
        resp = self.delete_user(user_id=user_id)
        assert "Successfully deleted" in resp
        assert user_id in resp

    def test_delete_not_exist_user(self):
        user_id = str(uuid4())
        resp = self.delete_user(user_id=user_id, expected_status=404)
        assert user_id in resp
        assert "not found" in resp


class TestMockChangeUser(BaseCase):
    @pytest.fixture()
    def prepare_mock(self):
        user_before = self.generate_user()
        self.send_user_in_mock(user_before)
        return user_before

    def test_change_user_valid_all_fields(self, prepare_mock):
        user_id = prepare_mock["id"]

        user_after = self.generate_user()
        payload = {"id": user_id, "name": user_after["name"], "surname": user_after['surname']}
        resp = self.change_user(payload=payload, expected_status=200)
        assert "Successfully update" in resp
        assert USER_DATA[user_id]["name"] == user_after["name"]
        assert USER_DATA[user_id]["surname"] == user_after["surname"]

    def test_change_user_valid_only_name(self, prepare_mock):
        user_id = prepare_mock["id"]

        user_after = self.generate_user()
        payload = {"id": user_id, "name": user_after["name"]}
        resp = self.change_user(payload=payload, expected_status=200)
        assert "Successfully update" in resp
        assert USER_DATA[user_id]["name"] == user_after["name"]
        assert USER_DATA[user_id]["surname"] == prepare_mock["surname"]

    def test_change_user_valid_only_surname(self, prepare_mock):
        user_id = prepare_mock["id"]

        user_after = self.generate_user()
        payload = {"id": user_id, "surname": user_after["surname"]}
        resp = self.change_user(payload=payload, expected_status=200)
        assert "Successfully update" in resp
        assert USER_DATA[user_id]["name"] == prepare_mock["name"]
        assert USER_DATA[user_id]["surname"] == user_after["surname"]

    def test_change_user_exist_fields(self, prepare_mock):
        user_id = prepare_mock["id"]

        payload = {"id": user_id}
        resp = self.change_user(payload=payload, expected_status=200)
        assert "Successfully update" in resp
        assert USER_DATA[user_id]["name"] == prepare_mock["name"]
        assert USER_DATA[user_id]["surname"] == prepare_mock["surname"]

    def test_change_user_with_not_exist_id(self):
        user_id = str(uuid4())
        resp = self.change_user(payload={"id": user_id}, expected_status=404)
        assert f"User with id {user_id} not found" == resp

    def test_change_user_without_id(self):
        resp = self.change_user(payload={}, expected_status=400)
        assert "Filed 'id' mast have in payload" == resp

    def test_change_user_no_valid_type_name(self, prepare_mock):
        user_id = prepare_mock["id"]

        payload = {"id": user_id, "name": 133}
        resp = self.change_user(payload=payload, expected_status=400)
        assert "Filed name must be str" == resp

    def test_change_user_no_valid_type_surname(self, prepare_mock):
        user_id = prepare_mock["id"]

        payload = {"id": user_id, "surname": 133}
        resp = self.change_user(payload=payload, expected_status=400)
        assert "Filed surname must be str" == resp
