import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

HOSTNAME = "127.0.0.1"
PORT = "3306"
DATABASE = "HomeWork2"
USERNAME = "root"
PASSWORD = "cuijianbin123"

DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8". \
    format(username=USERNAME, password=PASSWORD, host=HOSTNAME, port=PORT, db=DATABASE) #Connect

engine = create_engine(DB_URI, echo=False)  # 引擎

Session = scoped_session(sessionmaker(bind=engine)  )# 会话

session = Session()  # 实例化

Base = declarative_base()  # Base

