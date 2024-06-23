from src.database.dbConnectionHandler import DBConnHandler
from src.models.advogadosModel import Advogado

from sqlalchemy.orm.exc import NoResultFound


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

    def insereNovoAdvogado(self, novoAdvogado: Advogado):
        try:
            with DBConnHandler() as db:
                db.session.add(novoAdvogado)
                print("\n\n1 ---------- Chegou aqui...")
                db.session.commit()
                print("2 ----------- Chegou aqui...")
                db.session.refresh(novoAdvogado)
                print("3 ----------- Chegou aqui...")

                return novoAdvogado
        except NoResultFound:
            return None
        except Exception as err:
            print(f"\n\n\terr - {err}")
            db.session.rollback()
            return err