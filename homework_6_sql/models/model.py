from constans.db_constants import TablesName
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

tables_agrs = {'mysql_charset': 'utf8'}


class LineCount(Base):
    __tablename__ = TablesName.LINE_COUNT.value
    __table_args__ = tables_agrs

    def __repr__(self):
        return f"<LineCount(" \
               f"id='{self.id}'" \
               f"line_count='{self.line_count}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    line_count = Column(Integer, nullable=False)


class MethodsCount(Base):
    __tablename__ = TablesName.METHOD_COUNT.value
    __table_args__ = tables_agrs

    def __repr__(self):
        return f"<MethodsCount(" \
               f"id='{self.id}', " \
               f"method_name='{self.method_name}', " \
               f"method_count='{self.method_count}'," \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    method_name = Column(String(20), nullable=False)
    method_count = Column(Integer, nullable=False)


class MostCommonUrl(Base):
    __tablename__ = TablesName.MOST_COMMON_URL.value
    __table_args__ = tables_agrs

    def __repr__(self):
        return f"<Most common url(" \
               f"id='{self.id}', " \
               f"url='{self.url}', " \
               f"count='{self.count}'," \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(200))
    count = Column(Integer)


class BadRequestTopMaxSize(Base):
    __tablename__ = TablesName.BAR_REQUEST_TOP_MAX_SIZE.value
    __table_args__ = tables_agrs

    def __repr__(self):
        return f"<BadRequestTopMaxSize(" \
               f"id='{self.id}'," \
               f"request_ip='{self.request_ip}', " \
               f"response_rc='{self.response_rc}', " \
               f"response_size='{self.request_size}', " \
               f"request_url='{self.request_url}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    request_ip = Column(String(30), nullable=False)
    response_rc = Column(Integer, nullable=False)
    request_size = Column(Integer, nullable=False)
    request_url = Column(String(1000), nullable=False)


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
