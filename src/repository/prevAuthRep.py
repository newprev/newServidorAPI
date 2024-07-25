import datetime

from dateutil.relativedelta import relativedelta
from sqlalchemy.exc import IntegrityError

from src.database.dbConnectionHandler import DBConnHandler
from src.models.advogadosModel import Advogado
from src.models.prevAuthModel import PrevAuth

from sqlalchemy.orm.exc import NoResultFound

from src.models.prevAuthSchema import CodAcessoSchema
from src.models.trocaSenhaModel import TrocaSenha
from src.models.trocaSenhaSchema import TrocaSenhaSchema


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

    def buscaAdvogadoPorCPF(self, cpfAdvogado: str, confirmado: bool = None, ativo: bool = None) -> Advogado:
        try:
            with DBConnHandler() as db:
                data = db.session.query(Advogado).filter(Advogado.cpf == cpfAdvogado)

                if confirmado is not None:
                    data = data.filter(Advogado.confirmado == confirmado)

                if ativo is not None:
                    data = data.filter(Advogado.ativo == ativo)

                return data.one()
        except NoResultFound:
            return None
        except Exception as err:
            db.session.rollback()
            return err

    def buscaAdvogadoPorEmail(self, emailAdvogado: str, confirmado: bool = None, ativo: bool = None) -> Advogado:
        try:
            with DBConnHandler() as db:
                data = db.session.query(Advogado).filter(Advogado.email == emailAdvogado)

                if confirmado is not None:
                    data = data.filter(Advogado.confirmado == confirmado)

                if ativo is not None:
                    data = data.filter(Advogado.ativo == ativo)

                return data.one()
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

    def buscaConfirmaCodPrimeiroAcesso(self, infoCodAcesso: CodAcessoSchema) -> bool:
        try:
            with DBConnHandler() as db:
                data = db.session.query(TrocaSenha).filter(
                    TrocaSenha.codAcesso == infoCodAcesso.codigo,
                    TrocaSenha.escritorioId == TrocaSenha.escritorioId,
                    TrocaSenha.primAcesso == True,
                    TrocaSenha.verificado == False
                )

                if infoCodAcesso.advogadoId is not None:
                    data = data.filter(TrocaSenha.advogadoId == infoCodAcesso.advogadoId)

                trocaSenha: TrocaSenha = data.one()
                tempoDecorrido: relativedelta = relativedelta(datetime.timezone.now(), trocaSenha.dataCadastro)
                if tempoDecorrido.minutes < 10:
                    trocaSenha.verificado = True

                    db.session.refresh(trocaSenha)
                    db.session.commit()
                    return True

                db.session.rollback()
                return False

        except NoResultFound as err:
            print(f"buscaConfirmaCodPrimeiroAcesso: err: {err}")
            db.session.rollback()
            return False

        except Exception as err:
            print(f"buscaConfirmaCodPrimeiroAcesso: err: {err}")
            db.session.rollback()
            return False

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