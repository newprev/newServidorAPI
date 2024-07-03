from typing import Callable
from sqlalchemy.orm.exc import NoResultFound

from src.database.dbConnectionHandler import DBConnHandler


def newPrevSessao(func: Callable, *args, **kwargs):
    print(f"{args=}")
    print(f"{kwargs=}")



    def criaSession(*args, **kwargs):
        print("1 -----------------------")
        try:
            print("2 -----------------------")
            with DBConnHandler() as db:
                print("3 -----------------------")
                return func(db)

        except NoResultFound:
            return None

        except Exception as err:
            db.session.rollback()
            return err

    return criaSession
