from sqlalchemy.exc import IntegrityError

from src.database.dbConnectionHandler import DBConnHandler
from src.models.escritoriosModel import Escritorio
from src.models.enderecoModel import Endereco

from sqlalchemy.orm.exc import NoResultFound


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

    def insreNovoEscritorio(self, novoEscritorio: Escritorio, novoEndereco: Endereco) -> dict:
        try:
            with DBConnHandler() as db:
                # Insere novo escritorio
                db.session.add(novoEscritorio)
                db.session.commit()
                db.session.refresh(novoEscritorio)

                # Insere novo endereco
                novoEndereco.escritorioId = novoEscritorio.escritorioId
                db.session.add(novoEndereco)
                db.session.commit()

                return {
                    'novoEndereco': novoEndereco.toDict(),
                    'novoEscritorio': novoEscritorio.toDict()
                }

        except IntegrityError as err:
            argErr: str = err.args[0]

            if 'Duplicate entry' in argErr:
                print(f"Chave duplicada\t")

            print(f"\n[IntegrityError] insreNovoEscritorio - err: {err}")
            db.session.rollback()
            return None

        except Exception as err:
            print(f"\n[Exception] insreNovoEscritorio - err: {err} ")
            db.session.rollback()
            return None

    def deletaEscritorioPorId(self, escritorioId: int) -> int:
        try:
            with DBConnHandler() as db:
                escritorioBuscado = db.session.query(Escritorio).filter(Escritorio.escritorioId == escritorioId)
                escritorioExiste: bool = db.session.query(escritorioBuscado.exists()).scalar()

                if escritorioExiste:
                    escritorioBuscado.delete()
                    db.session.commit()
                    return escritorioId

                return -1

        except NoResultFound:
            return None