from constans.db_constants import TablesName
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta
Base: DeclarativeMeta = declarative_base()

tables_agrs = {'mysql_charset': 'utf8'}


class LineCount(Base):
    __tablename__ = TablesName.LINE_COUNT.value
    __table_args__ = tables_agrs

    def __repr__(self):
        return f"<LineCount(" \
               f"count='{self.line_count}'" \
               f")>"

    line_count = Column(Integer)


class MethodsCount(Base):
    __tablename__ = TablesName.LINE_COUNT.value
    __table_args__ = tables_agrs

    def __repr__(self):
        return f"<MethodsCount(" \
               f"method_name='{self.method_name}', " \
               f"method_count='{self.method_count}'," \
               f")>"

    method_name = Column(String(20))
    method_count = Column(Integer)


class MostCommonUrl(Base):
    __tablename__ = TablesName.MOST_COMMON_URL.value
    __table_args__ = tables_agrs

    def __repr__(self):
        return f"<Most common url(" \
               f"url='{self.url}', " \
               f"count='{self.count}'," \
               f")>"

    count = Column(Integer)
    url = Column(String(200))


class BadRequestTopMaxSize(Base):
    __tablename__ = TablesName.BAR_REQUEST_TOP_MAX_SIZE.value
    __table_args__ = tables_agrs

    def __repr__(self):
        return f"<BadRequestTopMaxSize(" \
               f"id='{self.id}'," \
               f"request_ip='{self.request_ip}', " \
               f"response_rc='{self.response_rc}', " \
               f"response_size='{self.response_size}', " \
               f"request_url='{self.request_url}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    request_ip = Column(String(30), nullable=False)
    response_rc = Column(Integer, nullable=False)
    response_size = Column(Integer, nullable=False)
    request_url = Column(String(200), nullable=False)


class ServerErrorTopIp(Base):
    __tablename__ = TablesName.SERVER_ERROR_TOP_IP.value
    __table_args__ = tables_agrs

    def __repr__(self):
        return f"<ServerErrorTopIp(" \
               f"id='{self.id}'," \
               f"request_ip='{self.request_ip}', " \
               f"count='{self.count}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    request_ip = Column(String(30), nullable=False)
    count = Column(Integer, nullable=False)
