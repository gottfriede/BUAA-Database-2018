from sqlalchemy import Column, Integer, String, VARCHAR, Enum

from Class.Father import Father


class Developer(Father):
    __tablename__ = "Developer"
    developerID = Column(Integer, primary_key=True, autoincrement=True)  # 默认不可为空
    developerName = Column(VARCHAR(50))
    developerPassword = Column(VARCHAR(50))
    developerTel = Column(VARCHAR(20), nullable=True)
    developerGraph = Column(VARCHAR(300), nullable=True)
