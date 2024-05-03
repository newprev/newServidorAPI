from database.dbConnectionHandler import DBConnHandler
from models.enderecoModel import Endereco

from sqlalchemy.orm.exc import NoResultFound


class EnderecoRepository:
    def selectAll(self):
        try:
            with DBConnHandler() as db:
                data = db.session.query(Endereco).all()
                return data

        except NoResultFound:
            return None

        except Exception as err:
            db.session.rollback()
            return err

    def buscaEnderecoPorId(self, enderecoId: int):
        try:
            with DBConnHandler() as db:
                data = db.session.query(Endereco).filter(Endereco.enderecoId == enderecoId).one()
                return data

        except NoResultFound:
            return None

        except Exception as err:
            db.session.rollback()
            return err