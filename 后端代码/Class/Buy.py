from sqlalchemy import Column, Integer, String, VARCHAR, Enum, and_

from Class.User2Game import User2Game
from Mysql import session
from Class.Father import Father


class Buy(Father):
    __tablename__ = "Buy"
    buyID = Column(Integer, primary_key=True, autoincrement=True)  # 默认不可为空
    buyTime = Column(VARCHAR(30))
    userID = Column(Integer)
    gameID = Column(Integer)
    status = Column(Enum("confirmed", "unconfirmed"))

