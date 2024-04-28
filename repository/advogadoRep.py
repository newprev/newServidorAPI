from database.dbConnectionHandler import DBConnHandler
from models.advogadosModel import Advogado


class AdvogadoRepository:
    def selectAll(self):
        with DBConnHandler() as db:
            data = db.session.query(Advogado).all()
            return data