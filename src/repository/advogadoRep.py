from pprint import pprint

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from datetime import datetime

from src.database.dbConnectionHandler import DBConnHandler
from src.models.advogadosModel import Advogado
from src.models.auxiliares.AdvogadoEscritorioSchema import AdvogadoEscritorio
from src.models.enderecoModel import Endereco
from src.models.escritorioModel import Escritorio


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
        with DBConnHandler() as db:
            try:
                novoAdvogado.senha = 'senhaTemp'

                db.session.add(novoAdvogado)
                db.session.flush()
                db.session.refresh(novoAdvogado)
                db.session.commit()
                db.session.expunge(novoAdvogado)

            except NoResultFound:
                return None
            except Exception as err:
                print(f"insereNovoAdvogado: err - {err}")
                db.session.rollback()
                return None

        return novoAdvogado


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

    def buscaAdvogadoEscritorio(self, advogadoId: int) -> AdvogadoEscritorio:
        with DBConnHandler() as db:
            try:
                advogadoEncontrado: Advogado = db.session.get_one(Advogado, advogadoId)
                if advogadoEncontrado is None:
                    raise NoResultFound

                escritorioEncontrado: Escritorio = db.session.get_one(Escritorio, advogadoEncontrado.escritorioId)
                if escritorioEncontrado is None:
                    raise NoResultFound

                enderecoDoEscritorio: Endereco = db.session.query(Endereco).filter(Endereco.escritorioId == advogadoEncontrado.escritorioId).one()
                if escritorioEncontrado is None:
                    raise NoResultFound

                return AdvogadoEscritorio(**{
                    'advogado': advogadoEncontrado.toDict(),
                    'escritorio': escritorioEncontrado.toDict(),
                    'endereco': enderecoDoEscritorio.toDict()
                })
            except NoResultFound:
                return None
