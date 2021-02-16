from sqlalchemy import Column, Integer, String, VARCHAR, Enum

from Class.Father import Father


class User2Game(Father):
    __tablename__ = "User2Game"
    # includeID = Column(Integer, primary_key=True, autoincrement=True)  # 默认不可为空

    userID = Column(Integer, primary_key=True)
    gameID = Column(Integer, primary_key=True)
