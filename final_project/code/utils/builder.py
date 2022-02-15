from dataclasses import dataclass

import faker

fake = faker.Faker()


class Builder:

    @staticmethod
    def user_data(username=None, email=None, password=None, confirm_password=None, access=1):

        @dataclass
        class CreateUser:
            username: str = None
            email: str = None
            password: str = None
            confirm_password: str = None
            access: int = 1

        if username is None:
            username = fake.user_name()

        if email is None:
            email = fake.ascii_email()

        if password is None:
            password = fake.bothify(text='???#??##$!###')

        if confirm_password is None:
            confirm_password = password

        return CreateUser(
            username=username,
            email=email,
            password=password,
            confirm_password=confirm_password,
            access=access
        )
