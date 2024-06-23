from src.database.dbConnectionHandler import DBConnHandler
from src.models.enderecoModel import Endereco

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

    def buscaPorEscritorioId(self, escritorioId: int):
        try:
            with DBConnHandler() as db:
                data = db.session.query(Endereco).filter(Endereco.escritorioId == escritorioId).all()
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
                data = db.session.query(Endereco).filter(Endereco.advogadoId == advogadoId).all()
                if len(data) == 0:
                    raise NoResultFound

                return data

        except NoResultFound:
            return None

        except Exception as err:
            db.session.rollback()
            return err