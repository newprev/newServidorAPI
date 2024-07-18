from pprint import pprint

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from datetime import datetime

from src.database.dbConnectionHandler import DBConnHandler
from src.models.advogadosModel import Advogado


class AdvogadoRepository:
    def selectAll(self, limit: int, offset: int):
        try:
            with DBConnHandler() as db:
                data = db.session.query(Advogado).limit(limit).offset(offset).all()
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

    def insereNovoAdvogado(self, novoAdvogado: Advogado):
        try:
            with DBConnHandler() as db:
                novoAdvogado.senha = 'senhaTemp'
                db.session.add(novoAdvogado)
                db.session.flush()
                db.session.commit()

                return novoAdvogado
        except NoResultFound:
            return None

        except Exception as err:
            print(f"\n\n\terr - {err}")
            db.session.rollback()
            return err

    def alteraAdvogado(self, advogadoId: int, advAlteracoes: Advogado):
        with DBConnHandler() as db:
            try:
                advogadoAtual: Advogado = db.session.query(Advogado).get(advogadoId)

                for chave, valor in advAlteracoes.toDict().items():
                    if valor is not None and chave != 'advogadoId':
                        setattr(advogadoAtual, chave, valor)

                advogadoAtual.dataUltAlt = datetime.now()

                db.session.flush()
                db.session.commit()
                db.session.refresh(advogadoAtual)

                return advogadoAtual

            except NoResultFound:
                return None

            except IntegrityError:
                print("alteraAdvogado - Erro de integridade do banco.")
                db.session.rollback()
                return None

            except Exception as err:
                print(f"\n\n\terr - {err=}")
                db.session.rollback()
                return None