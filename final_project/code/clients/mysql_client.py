import enum
from typing import Callable

import faker
import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker

import utils.utils
from constants.app_constants import TablesName, DbProperty, DefaultUser
from db_models.models import Base, TestUsers
from utils.builder import Builder


class MysqlORMClient:

    def __init__(self, user, password, db_name, host=DbProperty.HOST, port=DbProperty.DB_PORT):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = host
        self.port = port

        self.engine = None
        self.connection = None
        self.session = None
        self.faker = faker.Faker()

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'

        self.engine = sqlalchemy.create_engine(url, encoding='utf8')
        self.connection = self.engine.connect()

        sm = sessionmaker(bind=self.connection.engine)  # session creation wrapper
        self.session = sm()

    def recreate_db(self):
        try:
            self.connect(db_created=False)
            self.execute_query(f'DROP database if exists {self.db_name}', fetch=False)
            self.execute_query(f'CREATE database {self.db_name}', fetch=False)

        finally:
            self.connection.close()

    def execute_query(self, query, fetch=True):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def prepare_create_tables(self):
        for table in TablesName:
            table: enum.Enum
            if not inspect(self.engine).has_table(table.value):
                Base.metadata.tables[table.value].create(self.engine)
        self.insert_data(
            model=TestUsers,
            username=DefaultUser.USERNAME,
            password=DefaultUser.PASSWORD,
            email=DefaultUser.EMAIL,
            access=1,
            active=1
        )

    def insert_data(self, model: Callable, **kwargs):
        table = model(**kwargs)
        self.session.add(table)
        self.session.commit()
        return table

    def get_all_users(self):
        self.session.commit()
        all_records = self.session.query(TestUsers).all()
        return all_records

    def check_user_in_db(
            self,
            username: str,
            password=None,
            email=None,
            access=None,
            active=None,
            start_active_time=None
    ):
        self.session.commit()
        all_users: TestUsers = self.session.query(TestUsers).filter_by(username=username).all()
        res = []
        check_username = len(all_users) == 1
        res.append(check_username)

        if password:
            check_password = password == all_users[0].password
            res.append(check_password)
        if email:
            check_email = email == all_users[0].email
            res.append(check_email)
        if access:
            check_access = access == all_users[0].access
            res.append(check_access)
        if active:
            check_active = active == all_users[0].active
            res.append(check_active)
        if start_active_time:
            check_start_active_time = start_active_time == str(all_users[0].start_active_time)
            res.append(check_start_active_time)

        return res

    def add_user(
            self,
            username: str = None,
            password: str = None,
            email: str = None,
            access: int = 1
    ):
        user_data = Builder().user_data(username=username, email=email, password=password, access=access)
        self.insert_data(
            TestUsers,
            username=user_data.username,
            password=user_data.password,
            email=user_data.email,
            access=user_data.access
        )
        return user_data
