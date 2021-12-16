import enum
from typing import Callable

import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker

from constans.db_constants import DbProperty
from constans.db_constants import TablesName
from models.model import Base


class MysqlORMClient:

    def __init__(self, user, password, db_name, host=DbProperty.DB_HOST.value, port=DbProperty.DB_PORT.value):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = host
        self.port = port

        self.engine = None
        self.connection = None
        self.session = None

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

    def insert_data(self, model: Callable, **kwargs):
        table = model(**kwargs)
        self.session.add(table)
        self.session.commit()
        return table
