from src.database.dbConnectionHandler import DBConnHandler
from src.models.contatoModel import Contato

from sqlalchemy.orm.exc import NoResultFound


class ContatoRepository:
    def selectAll(self):
        try:
            with DBConnHandler() as db:
                data = db.session.query(Contato).all()
                return data

        except NoResultFound:
            return None

        except Exception as err:
            db.session.rollback()
            return err

    def buscaContatoPorId(self, contatoId: int):
        try:
            with DBConnHandler() as db:
                data = db.session.query(Contato).filter(Contato.contatoId == contatoId).one()
                return data

        except NoResultFound:
            return None

        except Exception as err:
            db.session.rollback()
            return err

    def buscaPorEscritorioId(self, contatoId: int):
        try:
            with DBConnHandler() as db:
                data = db.session.query(Contato).filter(Contato.contatoId == contatoId).all()
                if len(data) == 0:
                    raise NoResultFound

                return data

        except NoResultFound:
            return None

        except Exception as err:
            db.session.rollback()
            return err

    def buscaPorAdvogadoId(self, advogadoId: int):
        try:
            with DBConnHandler() as db:
                data = db.session.query(Contato).filter(Contato.advogadoId == advogadoId).all()
                if len(data) == 0:
                    raise NoResultFound

                return data

        except NoResultFound:
            return None

        except Exception as err:
            db.session.rollback()
            return err