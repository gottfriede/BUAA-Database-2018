from sqlalchemy import Column, Integer, String, VARCHAR, Enum, Float

from Class.Father import Father


class Game(Father):
    __tablename__ = "Game"
    gameID = Column(Integer, primary_key=True, autoincrement=True)  # 默认不可为空
    gameName = Column(VARCHAR(50))
    gamePrice = Column(Integer)
    introduction = Column(VARCHAR(50), nullable=True)
    gradeAvg = Column(Float, nullable=True) #总评分
    gameType = Column(Enum('action', 'adventure', 'cosplay', 'simulation', 'relaxation', 'else'))
    developerID = Column(Integer)
    gameGraph = Column(VARCHAR(300),nullable=True)#地址
    gameDetailGraph = Column(VARCHAR(300),nullable=True) #详细地址