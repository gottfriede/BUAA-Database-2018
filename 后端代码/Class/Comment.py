from sqlalchemy import Column, Integer, String, VARCHAR, Enum

from Class.Father import Father


class Comment(Father):
    __tablename__ = "Comment"
    commentID = Column(Integer, primary_key=True, autoincrement=True)  # 默认不可为空
    commentContents = Column(VARCHAR(251))
    commentTime = Column(VARCHAR(30))
    userID = Column(Integer)
    gameID = Column(Integer)
    grade = Column(Enum('1', '2', '3', '4', '5'))
