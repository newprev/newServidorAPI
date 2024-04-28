from database.dbConnectionHandler import DBConnHandler
from models.escritoriosModel import Escritorio


class EscritorioRepository:
    def selectAll(self):
        with DBConnHandler() as db:
            data = db.session.query(Escritorio).all()
            return data