from database.dbConnectionHandler import DBConnHandler
from models.escritoriosModel import Escritorio

from sqlalchemy.orm.exec import NoResultFound


class EscritorioRepository:
    def selectAll(self):
        try:
            with DBConnHandler() as db:
                data = db.session.query(Escritorio).all()
                return data
        except NoResultFound:
            return None
        except Exception as err:
            db.session.rollback()
            return err

    def buscaEscritorioPorId(self, escritorioId: int):
        try:
            with DBConnHandler() as db:
                data = db.session.query(Escritorio).filter(Escritorio.escritorioId == escritorioId).one()
                return data
        except NoResultFound:
            return None
        except Exception as err:
            db.session.rollback()
            return err