from Mysql import session


##############  触发器  ##################
def afterDeleteBuy():
    session.execute("DROP TRIGGER IF EXISTS afterDeleteBuy")
    session.commit()
    afterDeleteBuy = "CREATE TRIGGER afterDeleteBuy before DELETE " \
                     "ON Buy FOR EACH ROW " \
                     "BEGIN " \
                     "DELETE FROM User2Game WHERE gameID = old.gameID and userID = old.userID; " \
                     "END;"

    session.execute(afterDeleteBuy)
    session.commit()


def afterDeleteGame():
    session.execute("DROP TRIGGER IF EXISTS afterDeleteGame")
    session.commit()
    afterDeleteGame = "CREATE TRIGGER afterDeleteGame before DELETE " \
                      "ON Game FOR EACH ROW " \
                      "BEGIN " \
                      "DELETE FROM Buy WHERE gameID = old.gameID ; " \
                      "DELETE FROM Comment WHERE gameID = old.gameID ; " \
                      "DELETE FROM Favorite2Game WHERE gameID = old.gameID ; " \
                      "DELETE FROM User2Game WHERE gameID = old.gameID ; " \
                      "END;"

    session.execute(afterDeleteGame)
    session.commit()

#
def afterDeleteUser():
    session.execute("DROP TRIGGER IF EXISTS afterDeleteUser")
    session.commit()
    afterDeleteUser = "CREATE TRIGGER afterDeleteUser before DELETE " \
                      "ON User FOR EACH ROW " \
                      "BEGIN " \
                      "DELETE FROM Buy WHERE userID = old.userID ; " \
                      "DELETE FROM Comment WHERE userID = old.userID ; " \
                      "DELETE FROM Favorite WHERE userID = old.userID ; " \
                      "DELETE FROM User2Game WHERE userID = old.userID ; " \
                      "END;"

    session.execute(afterDeleteUser)
    session.commit()


def afterDeleteDeveloper():
    session.execute("DROP TRIGGER IF EXISTS afterDeleteDeveloper")
    session.commit()
    afterDeleteDeveloper = "CREATE TRIGGER afterDeleteDeveloper before DELETE " \
                           "ON Developer FOR EACH ROW " \
                           "BEGIN " \
                           "DELETE FROM Game WHERE developerID = old.developerID ; " \
                           "END;"

    session.execute(afterDeleteDeveloper)
    session.commit()


def confirmBuy():  # 再confirmGame之后增加关系到user2Game中:
    session.execute("DROP TRIGGER IF EXISTS confirmBuy")
    session.commit()
    confirmBuy = "CREATE TRIGGER confirmBuy after UPDATE " \
                 "ON buy FOR EACH ROW " \
                 "BEGIN " \
                 "IF new.status = 'confirmed' AND NOT EXISTS(SELECT * FROM user2game" \
                 " WHERE userID = new.userID AND gameID = new.gameID) THEN " \
                 "INSERT INTO user2game(userID,gameID) " \
                 "VALUES (new.userID,new.gameID) ;" \
                 "end if; " \
                 "END;"

    session.execute(confirmBuy)
    session.commit()
