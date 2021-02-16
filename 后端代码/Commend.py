# 推荐算法
class Commend():
    def __init__(self):
        self.User2Map = {}
        self.Game2Time = {}
        self.commentList = []  # 放gameID

    def deleteGame(self, id):
        if id in self.Game2Time.keys():
            self.Game2Time.pop(id)  # 移除
        if id in self.commentList:
            self.commentList.remove(id)

    def getCommentList(self):
        print(self.Game2Time)
        self.commentList = self.sort_by_value(self.Game2Time)
        return self.commentList

    def sort_by_value(self, d):
        items = d.items()
        backitems = [[v[1], v[0]] for v in items]
        backitems.sort(reverse=True)#从大到小排序
        return [backitems[i][1] for i in range(0, len(backitems))]  # 返回key
