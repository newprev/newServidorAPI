from database.dbConnectionHandler import DBConnHandler
from models.advogadosModel import Advogado

from sqlalchemy.orm.exec import NoResultFound


class AdvogadoRepository:
    def selectAll(self):
        try:
            with DBConnHandler() as db:
                data = db.session.query(Advogado).all()
                return data
        except NoResultFound:
            return None
        except Exception as err:
            db.session.rollback()
            return err


    def buscaPorId(self, advogadoId: int):
        try:
            with DBConnHandler() as db:
                data = db.session.query(Advogado).filter(Advogado.advogadoId == advogadoId).one()
                return data
        except NoResultFound:
            return None
        except Exception as err:
            db.session.rollback()
            return err