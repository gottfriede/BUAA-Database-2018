from sqlalchemy import Column, Integer, String, VARCHAR

from Class.Father import Father


class User(Father):
    __tablename__ = "User"
    userID = Column(Integer, primary_key=True, autoincrement=True)  # 默认不可为空
    userName = Column(String(50))
    userPassword = Column(String(50))
    email = Column(VARCHAR(30), nullable=True)
    userTel = Column(VARCHAR(20), nullable=True)
    userGraph = Column(VARCHAR(300), nullable=True)  # 地址
