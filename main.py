from pathlib import Path

import uvicorn
from fastapi import FastAPI

from controller.healthCheckController import healthCheckRouter
from controller.advogadoController import advogadoRouter
from controller.escritorioController import escritorioRouter
from controller.enderecoController import enderecoRouter

from models.advogadosModel import Advogado
from models.escritoriosModel import Escritorio
from models.enderecoModel import Endereco

app = FastAPI()

origens = [
    
]


#Incluindo rotas
app.include_router(healthCheckRouter)
app.include_router(advogadoRouter)
app.include_router(escritorioRouter)
app.include_router(enderecoRouter)


if __name__ == '__main__':
    from database.database import Base
    from database.dbConnectionHandler import DBConnHandler

    connHandler: DBConnHandler = DBConnHandler()

    Base.metadata.create_all(connHandler.get_engine())
    uvicorn.run(app, host='0.0.0.0', port=8000)
