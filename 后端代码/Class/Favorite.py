from sqlalchemy import Column, Integer, String, VARCHAR, Enum

from Class.Father import Father


class Favorite(Father):
    __tablename__ = "Favorite"
    favoriteID = Column(Integer, primary_key=True, autoincrement=True)  # 默认不可为空
    favoriteName = Column(VARCHAR(50))
    userID = Column(Integer)
