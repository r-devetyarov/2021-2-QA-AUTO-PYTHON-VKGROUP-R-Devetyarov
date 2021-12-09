from constants.app_constants import TablesName
from sqlalchemy import Column, Integer, String, Date, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

tables_agrs = {'mysql_charset': 'utf8'}


class   TestUsers(Base):
    __tablename__ = TablesName.TEST_USERS.value
    __table_args__ = tables_agrs

    def __repr__(self):
        return f"\n<LineCount(" \
               f"id='{self.id}'" \
               f"username='{self.username}'" \
               f"password='{self.password}'" \
               f"email='{self.email}'" \
               f"access='{self.access}'" \
               f"active='{self.active}'" \
               f"start_active_time='{self.start_active_time}'" \
               f")>\n"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), default=None, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    access = Column(SmallInteger, default=None)
    active = Column(SmallInteger, default=None)
    start_active_time = Column(Date, default=None)
