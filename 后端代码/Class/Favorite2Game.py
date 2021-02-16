from sqlalchemy import Column, Integer, String, VARCHAR, Enum

from Class.Father import Father


class Favorite2Game(Father): #包罗，从收藏夹到游戏
    __tablename__ = "Favorite2Game"
    # includeID = Column(Integer, primary_key=True, autoincrement=True)  # 默认不可为空

    favoriteID = Column(Integer, primary_key=True) #收藏夹ID
    gameID = Column(Integer, primary_key=True) #游戏ID
