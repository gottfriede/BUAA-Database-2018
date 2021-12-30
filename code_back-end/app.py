from __future__ import unicode_literals
import os
import time

from flask import *
from flask_cors import *
from sqlalchemy import and_, event

from Class.Comment import Comment
from Class.Developer import Developer
from Class.Favorite import Favorite
from Class.Favorite2Game import Favorite2Game
from Class.Game import Game
from Class.User import User
from Class.Buy import Buy
from Class.User2Game import User2Game
from Common import create_token, verify_token
from Mysql import session
from Main import com

# 配置
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, supports_credentials=True)
userGraphPath = os.path.join('static', 'User')
gameGraphPath = os.path.join('static', 'Game')
developerGraphPath = os.path.join('static', 'Developer')

# basepath = os.path.dirname(__file__)
basepath = '../sdeam'
adminCount = "cjbgtcyzm"
adminPassword = "wpbyyds"


@app.after_request
def af_request(resp):
    """
    #请求钩子，在所有的请求发生后执行，加入headers。
    :param resp:
    :return:
    """
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    return resp


def getUserID(userName):  # 获取用户ID
    ans = session.query(User.userID).filter(User.userName == userName).first()
    return int(ans[0])


def getDeveloperID(developerName):  # 获取DeveloperID
    ans = session.query(Developer.developerID).filter(Developer.developerName == developerName).first()[
        0]
    return int(ans)


def getGameID(gameName):  # 获取GameIqueD
    ans = session.query(Game.gameID).filter(Game.gameName == gameName).first()[0]
    return int(ans)


def gameGradeUpdate(gameID):
    commentList = session.query(Comment.grade).filter(Comment.gameID == gameID).all()
    gradeSum = 0
    number = 0
    for i in commentList:
        number += 1
        gradeSum += float(i[0])
    # 更新平均分
    if number == 0:
        gradeAvg = 0
    else:
        gradeAvg = round(float(gradeSum / number), 2)
    game = session.query(Game).filter(Game.gameID == gameID).first()  # 获取game
    game.gradeAvg = gradeAvg
    game.update()  # 更新游戏评分


@app.route('/userRegister', methods=['POST', 'GET'])  # 用户注册 done3
def UserRegister():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        userName = postForm['userName']
        password = postForm['password']
        email = postForm['email'] if 'email' in postForm else None
        userTel = postForm['userTel'] if 'userTel' in postForm else None
        if not session.query(User).filter(User.userName == userName).all():  # 未注册
            user = User(userName=userName, userPassword=password)
            if email:
                user.email = email
            if userTel:
                user.userTel = userTel
            user.save()
            userID = str(user.userID)
            return json.dumps({  # 返回json
                "userID": int(userID)
            }, ensure_ascii=False)
        else:
            print("name repeat")
            return "RepeatName", 400


@app.route('/developerRegister', methods=['POST', 'GET'])  # 商户注册 done3
def DeveloperRegister():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        developerName = postForm['developerName']
        password = postForm['password']
        developerTel = postForm['developerTel'] if 'developerTel' in postForm else None
        if not session.query(Developer).filter(Developer.developerName == developerName).all():  # 未注册
            developer = Developer(developerName=developerName, developerPassword=password)
            if developerTel:
                developer.developerTel = developerTel
            developer.save()
            developerID = str(developer.developerID)
            return json.dumps({  # 返回json
                "developerID": int(developerID)
            }, ensure_ascii=False)
        else:
            print("name repeat")
            return "RepeatName", 400


@app.route('/userLogin', methods=['POST', 'GET'])  # 查询用户表的某个用户 done3
def UserLogin():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        userName = postForm['userName']
        userPassword = postForm['userPassword']
        if not session.query(User).filter(User.userName == userName).all():  # 未注册
            print("NOT REGISTER")
            return "NotRegister", 400  # 还未注册
        else:
            ans = session.query(User.userPassword).filter(User.userName == userName).first()
            if ans[0] == userPassword:
                userID = getUserID(userName)
                if userID not in com.User2Map:
                    com.Game2Time.clear()
                    com.User2Map[userID] = com.Game2Time
                else:
                    com.Game2Time = com.User2Map[userID]
                # 设置返回
                token = create_token(userID)
                return json.dumps({
                    'userID': token
                }, ensure_ascii=False)
            else:
                print("WRONG PASSWORD")
                return "WrongPassWord", 400


@app.route('/changeUserInfor', methods=['POST', 'GET'])  # 用户信息更改 done3
def ChangeUserInfor():
    if request.method == 'POST':
        # 获取信息
        postForm = json.loads(request.get_data(as_text=True))
        userID = postForm['userID'] if 'userID' in postForm else None
        if not userID:
            "WITHOUT COOKIES", 400
        userID = verify_token(userID)
        userGraph = postForm['userGraph'] if 'userGraph' in postForm else None
        userTel = postForm['userTel'] if 'userTel' in postForm else None
        userPassword = postForm['userPassword'] if 'userPassword' in postForm else None
        email = postForm['email'] if 'email' in postForm else None
        userName = postForm['userName'] if 'userName' in postForm else None
        # 图片
        user = session.query(User).filter(User.userID == userID).first()
        if userGraph:
            user.userGraph = userGraph
        if userTel:
            user.userTel = userTel
        if userPassword:
            user.userPassword = userPassword
        if email:
            user.email = email
        if userName:
            user.userName = userName
        user.save()
        return "SUCCESS"


@app.route('/uploadUserGraph', methods=['POST', 'GET'])  # 用户信息更改 done3
def UploadUserGraph():
    if request.method == 'POST':
        img = request.files.get('userGraph')
        if img:
            if not os.path.exists(userGraphPath):
                os.makedirs(userGraphPath)
            uploadPath = os.path.join(basepath, userGraphPath, (img.filename))
            if os.path.exists(uploadPath):
                tmp = (img.filename).split('.')
                ticks = time.time()
                img.filename = tmp[0] + str(int(ticks)) + '.' + tmp[1]
                uploadPath = os.path.join(basepath, userGraphPath, (img.filename))
            img.save(uploadPath)
            uploadPath = '.' + uploadPath[8:]
            return json.dumps({
                'userGraphPath': uploadPath
            }, ensure_ascii=False)
        else:
            return "NO GRAPH", 400


@app.route('/changeGameInfor', methods=['POST', 'GET'])  # 游戏信息更改 done3
def ChangeGameInfor():
    if request.method == 'POST':
        # 获取信息
        postForm = json.loads(request.get_data(as_text=True))
        developerID = postForm['developerID'] if 'developerID' in postForm else None
        if not developerID:
            return "WITHOUT COOKIES", 400
        developerID = verify_token(developerID)
        gameID = postForm['gameID'] if 'gameID' in postForm else None
        gameName = postForm['gameName'] if 'gameName' in postForm else None
        gamePrice = int(postForm['gamePrice'] if 'gamePrice' in postForm else None)
        introduction = postForm['introduction'] if 'introduction' in postForm else None
        gameType = postForm['gameType'] if 'gameType' in postForm else None
        gameGraph = postForm['gameGraph'] if 'gameGraph' in postForm else None
        game = session.query(Game).filter(Game.gameID == gameID).first()
        if gameGraph:
            game.gameGraph = gameGraph
        if gameName:
            game.gameName = gameName
        if gamePrice:
            game.gamePrice = gamePrice
        if introduction:
            game.introduction = introduction
        if gameType:
            game.gameType = gameType
        game.save()
        return "SUCCESS"


@app.route('/uploadGameGraph', methods=['POST', 'GET'])  # 上传缩略图片 done3
def UploadGameGraph():
    if request.method == 'POST':
        img = request.files.get('gameGraph')
        if img:
            if not os.path.exists(gameGraphPath):
                os.makedirs(gameGraphPath)
            uploadPath = os.path.join(basepath, gameGraphPath, (img.filename))
            if os.path.exists(uploadPath):
                tmp = (img.filename).split('.')
                ticks = time.time()
                img.filename = tmp[0] + str(int(ticks)) + '.' + tmp[1]
                uploadPath = os.path.join(basepath, gameGraphPath, (img.filename))
            img.save(uploadPath)
            uploadPath = '.' + uploadPath[8:]
            return json.dumps({
                'gameGraphPath': uploadPath
            }, ensure_ascii=False)
        else:
            return "NO GRAPH", 400


@app.route('/uploadGameDetailGraph', methods=['POST', 'GET'])  # 上传详细图片 done3
def UploadGameDetailGraph():
    if request.method == 'POST':
        img = request.files.get('gameDetailGraph')
        if img:
            if not os.path.exists(gameGraphPath):
                os.makedirs(gameGraphPath)
            uploadPath = os.path.join(basepath, gameGraphPath, (img.filename))
            if os.path.exists(uploadPath):
                tmp = (img.filename).split('.')
                ticks = time.time()
                img.filename = tmp[0] + str(int(ticks)) + '.' + tmp[1]
                uploadPath = os.path.join(basepath, gameGraphPath, (img.filename))
            img.save(uploadPath)
            uploadPath = '.' + uploadPath[8:]
            return json.dumps({
                'gameDetailGraph': uploadPath
            }, ensure_ascii=False)
        else:
            return "NO GRAPH", 400


@app.route('/changeDeveloperInfor', methods=['POST', 'GET'])  # 游戏信息更改 done3
def ChangeDeveloperInfor():
    if request.method == 'POST':
        # 获取信息
        postForm = json.loads(request.get_data(as_text=True))
        developerID = postForm['developerID'] if 'developerID' in postForm else None
        if not developerID:
            return "WITHOUT COOKIES", 400
        developerID = verify_token(developerID)
        developerName = postForm['developerName'] if 'developerName' in postForm else None
        developerPassword = postForm['developerPassword'] if 'developerPassword' in postForm else None
        developerTel = postForm['developerTel'] if 'developerTel' in postForm else None
        developerGraph = postForm['developerGraph'] if 'developerGraph' in postForm else None
        #
        developer = session.query(Developer).filter(Developer.developerID == developerID).first()
        if developerGraph:
            developer.developerGraph = developerGraph
        if developerName:
            developer.developerName = developerName
        if developerPassword:
            developer.developerPassword = developerPassword
        if developerTel:
            developer.developerTel = developerTel
        developer.save()
        return "SUCCESS", 200


@app.route('/uploadDeveloperGraph', methods=['POST', 'GET'])  # 用户信息更改 done3
def UploadDeveloperGraph():
    if request.method == 'POST':
        img = request.files.get('developerGraph')
        if img:
            if not os.path.exists(developerGraphPath):
                os.makedirs(developerGraphPath)
            uploadPath = os.path.join(basepath, developerGraphPath, (img.filename))
            if os.path.exists(uploadPath):
                tmp = (img.filename).split('.')
                ticks = time.time()
                img.filename = tmp[0] + str(int(ticks)) + '.' + tmp[1]
                uploadPath = os.path.join(basepath, developerGraphPath, (img.filename))
            img.save(uploadPath)
            uploadPath = '.' + uploadPath[8:]
            return json.dumps({
                'developerGraphPath': uploadPath
            }, ensure_ascii=False)
        else:
            return "NO GRAPH", 400


@app.route('/developerLogin', methods=['POST', 'GET'])  # 查询开发者表的开发者 done
def DeveloperLogin():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        developerName = postForm['developerName']
        developerPassword = postForm['developerPassword']
        if not session.query(Developer).filter(Developer.developerName == developerName).all():  # 未注册
            print("NOT REGISTER")
            return "NotRegister", 400  # 还未注册
        else:
            ans = session.query(Developer.developerPassword).filter(Developer.developerName == developerName).first()
            if ans[0] == developerPassword:
                developerID = create_token(getDeveloperID(developerName))
                return json.dumps({
                    'developerID': developerID
                }, ensure_ascii=False)
            else:
                print("WRONG PASSWORD")
                return "WrongPassWord", 400


@app.route('/developerLogout', methods=['POST', 'GET'])  # 开发者推出，注销cookie done3
def DeveloperLogout():
    if request.method == 'POST':
        resp = make_response("DELETE SUCCESS")
        resp.delete_cookie("developerID")
        return resp


@app.route('/adminLogout', methods=['POST', 'GET'])  # 用户登出，注销cookie done3
def AdminLogout():
    if request.method == 'POST':
        resp = make_response("DELETE SUCCESS")
        resp.delete_cookie("admin")
        return resp


@app.route('/userLogout', methods=['POST', 'GET'])  # 用户登出，注销cookie done3
def UserLogout():
    if request.method == 'POST':
        resp = make_response("DELETE SUCCESS")
        resp.delete_cookie("userID")
        return resp


@app.route('/getUserTable', methods=['POST', 'GET'])  # 根据ID返回全部用户表内容 done3
def GetUserTable():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        userID = postForm['userID'] if 'userID' in postForm else None
        if not userID:
            return 'WITHOUT COOKIES', 400
        userID = verify_token(userID)
        user = session.query(User).filter(User.userID == userID).first()
        ansList = {
            'userName': user.userName,
            'email': user.email,
            'userTel': user.userTel,
            'userGraph': user.userGraph
        }
        return json.dumps(ansList, ensure_ascii=False);


@app.route('/queryDeveloperGames', methods=['POST', 'GET'])  # 根据姓名查询游戏报寒 done2
def QueryDeveloperGames():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        developerID = postForm['developerID'] if 'developerID' in postForm else None
        if not developerID:
            return 'WITHOUT COOKIES', 400
        developerID = verify_token(developerID)
        gameList = session.query(Game).filter(Game.developerID == developerID).all()
        ans = []
        for i in gameList:
            ans.append({
                'gameName': i.gameName,
                'gamePrice': i.gamePrice,
                'introduction': i.introduction,
                'gameType': i.gameType,
                'gameGraph': i.gameGraph
            })
        return json.dumps(ans, ensure_ascii=False)


@app.route('/queryUserGames', methods=['POST', 'GET'])  # 根据姓名查询游戏报寒 done2
def QueryUserGames():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        userID = postForm['userID'] if 'userID' in postForm else None
        if not userID:
            return 'WITHOUT COOKIES', 400
        userID = verify_token(userID)
        gameList = session.query(Game).filter(and_(User2Game.userID == userID, User2Game.gameID == Game.gameID)).all()
        ans = []
        for i in gameList:
            ans.append({
                'gameName': i.gameName,
                'gamePrice': i.gamePrice,
                'introduction': i.introduction,
                'gameType': i.gameType,
                'gameGraph': i.gameGraph,
                'gameID': i.gameID,
                'gameDetailGraph': i.gameDetailGraph
            })
        return json.dumps(ans, ensure_ascii=False)


@app.route('/uploadGame', methods=['POST', 'GET'])  # 上传游戏 done3
def UploadGame():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        developerID = postForm['developerID'] if 'developerID' in postForm else None
        if not developerID:
            return "WITHOUT COOKIES", 400
        developerID = verify_token(developerID)
        gameName = postForm['gameName'] if 'gameName' in postForm else None
        gamePrice = postForm['gamePrice'] if 'gamePrice' in postForm else None
        introduction = postForm['introduction'] if 'introduction' in postForm else None
        gameType = postForm['gameType'] if 'gameType' in postForm else None
        gameGraph = postForm['gameGraph'] if 'gameGraph' in postForm else None
        gameDetailGraph = postForm['gameDetailGraph'] if 'gameDetailGraph' in postForm else None

        if not developerID:  # 不存在这个开发者
            return "DeveloperNotExists", 400
        elif gameType not in ['action', 'adventure', 'cosplay', 'simulation', 'relaxation', 'else']:
            return "TypeError", 400
        else:
            if not session.query(Game).filter(Game.gameName == gameName).all():  # 未注册
                game = Game(gameName=gameName, gamePrice=gamePrice, gameType=gameType,
                            developerID=developerID)
                if introduction:
                    game.introduction = introduction
                if gameGraph:
                    game.gameGraph = gameGraph
                if gameDetailGraph:
                    game.gameDetailGraph = gameDetailGraph
                game.save()
                gameID = getGameID(gameName)
                return json.dumps({
                    "gameID": int(gameID)
                }, ensure_ascii=False)  # 必须要有return
            else:
                return "RepeatName", 400


@app.route('/createFavorite', methods=['POST', 'GET'])  # 用户添加收藏夹 done3
def CreateFavorite():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        userID = postForm['userID'] if 'userID' in postForm else None
        if not userID:
            return 'WITHOUT COOKIES', 400
        userID = verify_token(userID)
        favoriteName = postForm['favoriteName']
        if not session.query(Favorite).filter(Favorite.favoriteName == favoriteName).all():  # 未注册
            favorite = Favorite(favoriteName=favoriteName, userID=userID)
            favorite.save()  # 插入 收藏
            favoriteID = favorite.favoriteID
            return json.dumps({
                "favoriteID": int(favoriteID)
            }, ensure_ascii=False)
        else:
            return "RepeatName", 400


@app.route('/deleteFavorite', methods=['POST', 'GET'])  # 删除收藏夹 done3
def DeleteFavorite():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        userID = postForm['userID'] if 'userID' in postForm else None
        if not userID:
            return 'WITHOUT COOKIES', 400
        userID = verify_token(userID)
        postForm = json.loads(request.get_data(as_text=True))
        favoriteName = postForm['favoriteName']
        favorite = session.query(Favorite).filter(
            and_(Favorite.favoriteName == favoriteName, Favorite.userID == userID)).first()
        if not favorite:
            return "NOT EXIST", 400
        favorite.delete()
        return "SUCCESS"


@app.route('/buyGame', methods=['POST', 'GET'])  # 添加订单 done3
def BuyGame():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        userID = postForm['userID'] if 'userID' in postForm else None
        if not userID:
            return 'WITHOUT COOKIES', 400
        userID = verify_token(userID)
        gameName = postForm['gameName']
        if not session.query(Game).filter(Game.gameName == gameName).first():  # 游戏不存在
            return "NOT EXIST", 400
        gameID = getGameID(gameName)
        buyTime = str(time.asctime(time.localtime(time.time())))
        status = "unconfirmed"
        if session.query(Buy).filter(and_(Buy.gameID == gameID, Buy.userID == userID)).first():  # 已经拥有了
            return "ALREADY HAVE", 400
        buy = Buy(userID=userID, gameID=gameID, buyTime=buyTime, status=status)
        buy.save()
        return json.dumps({
            "buyID": int(buy.buyID),
            "buyTime": buyTime
        }, ensure_ascii=False)


@app.route('/confirmGame', methods=['POST', 'GET'])  # 确认游戏 done3
def ConfirmGame():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        userID = postForm['userID'] if 'userID' in postForm else None
        if not userID:
            return 'WITHOUT COOKIES', 400
        userID = verify_token(userID)
        buyID = postForm['buyID']
        buy = session.query(Buy).filter(Buy.buyID == buyID).first()  # 获取对象
        gameID = buy.gameID
        if not buy:
            return "BUY NOT EXIST", 400
        buy.status = 'confirmed'
        buy.update()
        com.deleteGame(gameID)  # 从推荐列表中移除该游戏
        return "SUCCESS", 200


@app.route('/deleteBuy', methods=['POST', 'GET'])  # 玩家删除订单 done3
def DeleteBuy():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        userID = postForm['userID'] if 'userID' in postForm else None
        if not userID:
            return 'WITHOUT COOKIES', 400
        userID = verify_token(userID)
        gameName = postForm['gameName']
        gameID = getGameID(gameName)
        buy = session.query(Buy).filter(and_(Buy.userID == userID, Buy.gameID == gameID)).first()
        buy.delete()  # 直接删除
        return "SUCCESS", 200


@app.route('/deleteGame', methods=['POST', 'GET'])  # 下架游戏 done3
def DeleteGame():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        developerID = postForm['developerID'] if 'developerID' in postForm else None
        if not developerID:
            return "WITHOUT COOKIES", 400
        developerID = verify_token(developerID)
        gameName = postForm['gameName']
        game = session.query(Game).filter(and_(Game.gameName == gameName, Game.developerID == developerID)).first()
        if not game:
            return "GAME NOT EXISTS", 400
        com.deleteGame(game.gameID)
        game.delete()
        return "SUCCESS", 200


@app.route('/adminDeleteGame', methods=['POST', 'GET'])  # 下架游戏 done3
def AdminDeleteGame():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        adminID = postForm['adminID'] if 'adminID' in postForm else None
        if not adminID:
            return "WITHOUT COOKIES", 400
        if int(adminID) != 996251:
            return "WRONG ANS", 400
        gameID = postForm['gameID']
        game = session.query(Game).filter(Game.gameID == gameID).first()
        if not game:
            return "GAME NOT EXISTS", 400
        com.deleteGame(game.gameID)
        game.delete()
        return "SUCCESS", 200


@app.route('/adminLogin', methods=['POST', 'GET'])  # 管理者登录 done
def AdminLogin():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        getAdminCount = postForm['adminCount']
        getAdminPassword = postForm['adminPassword']
        if (getAdminCount == adminCount) & (getAdminPassword == adminPassword):
            return json.dumps({
                'adminID': 996251
            }, ensure_ascii=False)
        else:
            return "WrongPassword", 400


@app.route('/addComment', methods=['POST', 'GET'])  # 添加评论 done3
def AddComment():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        userID = postForm['userID'] if 'userID' in postForm else None
        if not userID:
            return "WITHOUT COOKIES", 400
        userID = verify_token(userID)
        gameName = postForm['gameName'] if 'gameName' in postForm else None
        gameID = int(getGameID(gameName))
        if not session.query(Game).filter(Game.gameID == gameID).all():  # 游戏不存在
            return "GameNotExists", 400
        if session.query(Comment).filter(and_(Comment.gameID == gameID), Comment.userID == userID).first():
            return "REPEAT COMMENT", 400
        commentTime = str(time.asctime(time.localtime(time.time())))
        grade = str(postForm['grade'])  # 只接受整形
        commentContents = postForm['commentContents']
        comment = Comment(grade=grade, commentTime=commentTime, gameID=gameID, userID=userID,
                          commentContents=commentContents)
        comment.save()
        # 增加1点兴趣
        if gameID in com.Game2Time:
            com.Game2Time[gameID] += 1
        else:
            com.Game2Time[gameID] = 1
        gameGradeUpdate(gameID)
        return json.dumps({
            "commentID": int(comment.commentID)
        }, ensure_ascii=False)


@app.route('/deleteComment', methods=['POST', 'GET'])  # 删除评论 done3 todo优化更新变成触发器
def DeleteComment():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        userID = postForm['userID'] if 'userID' in postForm else None
        if not userID:
            return "WITHOUT COOKIES", 400
        userID = verify_token(userID)
        gameName = postForm['gameName']
        gameID = getGameID(gameName)
        comment = session.query(Comment).filter(and_(Comment.gameID == gameID, Comment.userID == userID)).first()
        comment.delete()
        gameGradeUpdate(gameID)
        return "SUCCESS"


@app.route('/addFavorite', methods=['POST', 'GET'])  # 添加游戏到收藏夹 done3
def AddFavorite():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        userID = postForm['userID'] if 'userID' in postForm else None
        if not userID:
            return "WITHOUT COOKIES", 400
        userID = verify_token(userID)
        favoriteName = postForm['favoriteName']
        gameName = postForm['gameName']
        gameID = getGameID(gameName)
        favoriteID = session.query(Favorite.favoriteID).filter(
            and_(Favorite.favoriteName == favoriteName, Favorite.userID == userID))
        if session.query(Favorite2Game).filter(and_(Favorite2Game.gameID == gameID),
                                               Favorite2Game.favoriteID == favoriteID).first():
            return "ALREADY HAVE", 400
        favorite2game = Favorite2Game(favoriteID=favoriteID, gameID=gameID)
        favorite2game.save()
        return "SUCCESS"


@app.route('/deleteGameFromFavroite', methods=['POST', 'GET'])  # 删除收藏 done3
def DeleteGameFromFavroite():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        userID = postForm['userID'] if 'userID' in postForm else None
        if not userID:
            return "WITHOUT COOKIES", 400
        userID = verify_token(userID)
        favoriteName = postForm['favoriteName']
        favoriteID = session.query(Favorite.favoriteID).filter(
            and_(Favorite.favoriteName == favoriteName, Favorite.userID == userID))
        gameName = postForm['gameName']
        gameID = getGameID(gameName)
        favorite2game = session.query(Favorite2Game).filter(
            and_(Favorite2Game.gameID == gameID, Favorite2Game.favoriteID == favoriteID)).first()
        favorite2game.delete()
        return "SUCCESS"


@app.route('/querySingleFavorite', methods=['POST', 'GET'])  # 查询单个收藏夹 返回游戏列表 done3
def QuerySingleFavorite():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        userID = postForm['userID'] if 'userID' in postForm else None
        if not userID:
            return "WITHOUT COOKIES", 400
        userID = verify_token(userID)
        favoriteID = postForm['favoriteID']
        ans = []
        gameList = []  # 游戏类列表
        gameIDList = session.query(Favorite2Game.gameID).filter(Favorite2Game.favoriteID == favoriteID).all()
        for i in gameIDList:
            gameList.append(session.query(Game).filter(Game.gameID == i[0]).first())
        for i in gameList:
            ans.append({
                'gameName': i.gameName,
                'introduction': i.introduction,
                'gameType': i.gameType,
                'gamePrice': i.gamePrice,
                'gameGraph': i.gameGraph,
                'gameDetailGraph': i.gameDetailGraph,
                'gameID': i.gameID
            })
        return json.dumps(ans, ensure_ascii=False)


@app.route('/queryUserFavorite', methods=['POST', 'GET'])  # 根据用户ID返回收藏夹信息 done3
def QueryUserFavorite():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        userID = postForm['userID'] if 'userID' in postForm else None
        if not userID:
            return "WITHOUT COOKIES", 400
        userID = verify_token(userID)
        favoriteList = session.query(Favorite).filter(Favorite.userID == userID).all()
        ans = []
        for i in favoriteList:
            ans.append({
                'favoriteID': i.favoriteID,
                'favoriteName': i.favoriteName
            })
        return json.dumps(ans, ensure_ascii=False)


@app.route('/queryAllGame', methods=['POST', 'GET'])  # 查询所有游戏信息 done3
def QueryAllGame():
    if request.method == 'POST':
        ans = []
        gameList = session.query(Game).all()  # 游戏列表
        commentList = com.getCommentList()
        sumList = []
        for i in commentList:
            sumList.append(session.query(Game).filter(Game.gameID == i).first())

        for i in gameList:
            if i.gameID not in commentList:
                sumList.append(i)
        for i in sumList:
            ans.append(
                {
                    "gameID": i.gameID,
                    "gameName": i.gameName,
                    "gameType": i.gameType,
                    "gamePrice": i.gamePrice,
                    "gameGraph": i.gameGraph
                })
        return json.dumps(ans, ensure_ascii=False)


@app.route('/queryBuy', methods=['POST', 'GET'])  # 查询用户下面的订单 done3
def QueryBuy():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        userID = postForm['userID'] if 'userID' in postForm else None
        if not userID:
            return "WITHOUT COOKIES", 400
        userID = verify_token(userID)
        ans = []
        buyList = session.query(Buy).filter(Buy.userID == userID).all()
        for i in buyList:
            gameName = session.query(Game.gameName).filter(Game.gameID == i.gameID).first()
            ans.append({
                "gameStatus": i.status,
                "gameName": gameName,
                "buyTime": i.buyTime,
            })
        return json.dumps(ans, ensure_ascii=False)


@app.route('/queryGame', methods=['POST', 'GET'])  # 查询游戏中详细信息(包括评分) done3
def QueryGame():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        userID = postForm['userID'] if 'userID' in postForm else None
        if not userID:
            return "WITHOUT COOKIES", 400
        userID = verify_token(userID)
        gameID = int(postForm['gameID'])
        if gameID in com.Game2Time:
            com.Game2Time[gameID] = com.Game2Time[gameID] + 1  # 浏览了一次
        else:
            com.Game2Time[gameID] = 1
        game = session.query(Game).filter(Game.gameID == gameID).first()
        developerName = \
            session.query(Developer.developerName).filter(Developer.developerID == game.developerID).first()[0]
        tmpComments = session.query(Comment).filter(Comment.gameID == gameID).all()
        userList = []
        for i in tmpComments:
            userList.append(session.query(User).filter(User.userID == i.userID).first())
        comments = []
        for i in range(len(userList)):
            comments.append({
                'userGraph': userList[i].userGraph,
                'userName': userList[i].userName,
                'comment': tmpComments[i].commentContents,
                'commentID': tmpComments[i].commentID
            })
        return json.dumps({
            "gameName": game.gameName,
            "gamePrice": game.gamePrice,
            "introduction": game.introduction,
            "gameType": game.gameType,
            "developerName": developerName,
            "gradeAvg": game.gradeAvg,
            "comments": comments,
            "gameGraph": game.gameGraph,
            "gameDetailGraph": game.gameDetailGraph
        }, ensure_ascii=False)


@app.route('/deleteUser', methods=['POST', 'GET'])  # 管理者删除用户
def DeleteUser():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        admin = postForm['adminID']
        if not admin:
            return "WITHOUT COOKIES", 400
        userID = postForm['userID']
        user = session.query(User).filter(User.userID == userID).first()
        if not user:
            return "USER NOT EXISTS", 400
        user.delete()
        return "SUCCESS", 200


@app.route('/deleteDeveloper', methods=['POST', 'GET'])  # 管理者删除游戏厂商
def DeleteDeveloper():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        admin = postForm['adminID']
        if not admin:
            return "WITHOUT COOKIES", 400
        developerID = postForm['developerID']
        developerID = verify_token(developerID)
        developer = session.query(Developer).filter(Developer.developerID == developerID).first()
        if not developer:
            return "DEVELOPER NOT EXISTS", 400
        developer.delete()
        return "SUCCESS", 200


@app.route('/adminDeleteComment', methods=['POST', 'GET'])  # 管理者删除评论
def AdminDeleteComment():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        admin = postForm['adminID']
        if not admin:
            return "WITHOUT COOKIES", 400
        commentID = postForm['commentID']
        comment = session.query(Comment).filter(Comment.commentID == commentID).first()
        if not comment:
            return "COMMENT NOT EXISTS", 400
        comment.delete()
        return "SUCCESS", 200


@app.route('/queryDeveloper', methods=['POST', 'GET'])  # 管理者删除评论
def QueryDeveloper():
    if request.method == 'POST':
        postForm = json.loads(request.get_data(as_text=True))
        developerID = postForm['developerID']
        if not developerID:
            return "WITHOUT COOKIES", 400
        developerID = verify_token(developerID)
        developer = session.query(Developer).filter(Developer.developerID == developerID).first()
        return json.dumps({
            'developerName': developer.developerName,
            'developerGraph': developer.developerGraph,
            'developerTel': developer.developerTel
        })
