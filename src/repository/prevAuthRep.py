import datetime

from sqlalchemy.exc import IntegrityError

from src.database.dbConnectionHandler import DBConnHandler
from src.models.advogadosModel import Advogado
from src.models.prevAuth import PrevAuth

from sqlalchemy.orm.exc import NoResultFound

from src.models.trocaSenhaModel import TrocaSenha, TrocaSenhaSchema


class PrevAuthRepository:
    def selectAll(self):
        try:
            with DBConnHandler() as db:
                data = db.session.query(PrevAuth).all()
                return data
        except NoResultFound:
            return None
        except Exception as err:
            db.session.rollback()
            return err

    def buscaPrevAuthPorId(self, authId: int):
        try:
            with DBConnHandler() as db:
                data = db.session.query(PrevAuth).filter(PrevAuth.authId == authId).one()
                return data
        except NoResultFound:
            return None
        except Exception as err:
            db.session.rollback()
            return err

    def buscaAdvogadoPorCPF(self, cpfAdvogado: str) -> Advogado:
        try:
            with DBConnHandler() as db:
                data = db.session.query(Advogado).filter(Advogado.cpf == cpfAdvogado).one()
                return data
        except NoResultFound:
            return None
        except Exception as err:
            db.session.rollback()
            return err

    def buscaAdvogadoPorEmail(self, emailAdvogado: str) -> Advogado:
        try:
            with DBConnHandler() as db:
                data = db.session.query(Advogado).filter(Advogado.email == emailAdvogado).one()
                return data
        except NoResultFound:
            return None
        except Exception as err:
            db.session.rollback()
            return err

    def salvaAdvogadoTrocaSenha(self, advogadoId: int, trocaSenhaModel: TrocaSenha) -> TrocaSenhaSchema:
        try:
            with (DBConnHandler() as db):
                # Atualiza Advogado
                advAtualizado: Advogado = db.session.query(Advogado).filter(Advogado.advogadoId == advogadoId).one()
                advAtualizado.confirmado = True
                advAtualizado.dataUltAlt = datetime.datetime.now()

                # Insere nova Troca de senha
                db.session.add(trocaSenhaModel)
                db.session.commit()

                return TrocaSenhaSchema(**trocaSenhaModel.toDict())

        except Exception as err:
            print(f"\n[Exception] salvaAdvogadoTrocaSenha - err: {err} ")
            db.session.rollback()
            return None

    # def insreNovoPrevAuth(self, prevAuth: PrevAuth) -> dict:
    #     try:
    #         with DBConnHandler() as db:
    #             # Insere novo escritorio
    #             db.session.add(novoEscritorio)
    #             db.session.commit()
    #             db.session.refresh(novoEscritorio)
    #
    #             # Insere novo endereco
    #             novoEndereco.escritorioId = novoEscritorio.escritorioId
    #             db.session.add(novoEndereco)
    #             db.session.commit()
    #
    #             return {
    #                 'novoEndereco': novoEndereco.toDict(),
    #                 'novoEscritorio': novoEscritorio.toDict()
    #             }
    #
    #     except IntegrityError as err:
    #         argErr: str = err.args[0]
    #
    #         if 'Duplicate entry' in argErr:
    #             print(f"Chave duplicada\t")
    #
    #         print(f"\n[IntegrityError] insreNovoEscritorio - err: {err}")
    #         db.session.rollback()
    #         return None
    #
    #     except Exception as err:
    #         print(f"\n[Exception] insreNovoEscritorio - err: {err} ")
    #         db.session.rollback()
    #         return None

    def deletaPrevAuthPorId(self, authId: int) -> int:
        try:
            with DBConnHandler() as db:
                authBuscado = db.session.query(PrevAuth).filter(PrevAuth.authId == authId)
                authExiste: bool = db.session.query(authBuscado.exists()).scalar()

                if authExiste:
                    authBuscado.delete()
                    db.session.commit()
                    return authId

                return -1

        except NoResultFound:
            return None