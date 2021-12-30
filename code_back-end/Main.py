from Mysql import *
from Trigger import *
from app import app
from Commend import *

com = Commend()  # 单例模式


def init():
    # 创建表
    Base.metadata.create_all(engine)

    # 创建触发器
    afterDeleteBuy()
    afterDeleteGame()
    afterDeleteUser()
    afterDeleteDeveloper()
    confirmBuy()


if __name__ == "__main__":
    init()
    app.run(debug='true')
