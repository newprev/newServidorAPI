from pprint import pprint
from typing import Union, Any

from sqlalchemy.exc import IntegrityError

from src.database.dbConnectionHandler import DBConnHandler
from src.models.erroSchema import NewPrevErro
from src.models.escritoriosModel import Escritorio
from src.models.enderecoModel import Endereco

from sqlalchemy.orm.exc import NoResultFound

from src.models.escritoriosSchema import EscritorioPostRequest


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

    def insreNovoEscritorio(self, novoEscritorio: Escritorio, novoEndereco: Endereco):
        with DBConnHandler() as db:
            try:
                # Insere novo escritorio
                db.session.add(novoEscritorio)
                db.session.flush()

                # Insere novo endereco
                novoEndereco.escritorioId = novoEscritorio.escritorioId
                db.session.add(novoEndereco)
                db.session.flush()

                # print(f"\n1 --------------------")
                # pprint(novoEndereco.toDict())
                # print(f"2 --------------------\n")

                db.session.commit()

                return EscritorioPostRequest(**{
                    'endereco': novoEndereco.toDict(),
                    'escritorio': novoEscritorio.toDict()
                })

            except IntegrityError as err:
                argErr: str = err.args[0]
                chaveDuplicada: bool = 'Duplicate entry' in argErr

                print(f"\n[IntegrityError] insreNovoEscritorio - err: {err}")

                # db.session.delete(novoEscritorio)
                db.session.rollback()

                return NewPrevErro(
                    erro=err,
                    detalhes=f"[IntegrityError] - {err.detail}",
                    observacao="Chave duplicada" if chaveDuplicada else None,
                    funcao="insreNovoEscritorio"
                )

            except KeyError as err:
                print(f"\n[KeyError] insreNovoEscritorio - err: {err} ")
                db.session.rollback()

                return NewPrevErro(
                    erro=err,
                    detalhes=f"[KeyError] - err: {err}",
                    funcao="insreNovoEscritorio",
                )

            except Exception as err:
                print(f"\n[Exception] insreNovoEscritorio - err: {err} ")

                db.session.rollback()

                return NewPrevErro(
                    erro=err,
                    detalhes=f"[Exception] - err: {err}",
                    funcao="insreNovoEscritorio",
                )



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