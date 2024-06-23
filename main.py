import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.controller.healthCheckController import healthCheckRouter
from src.controller.advogadoController import advogadoRouter
from src.controller.escritorioController import escritorioRouter
from src.controller.enderecoController import enderecoRouter
from src.controller.contatoController import contatoRouter
from src.controller.prevAuthController import prevAuthRouter

app = FastAPI()

origens = [
    '0.0.0.0:8000'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origens,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


#Incluindo rotas
app.include_router(healthCheckRouter)
app.include_router(advogadoRouter)
app.include_router(escritorioRouter)
app.include_router(enderecoRouter)
app.include_router(contatoRouter)
app.include_router(prevAuthRouter)


if __name__ == '__main__':
    from src.database.database import Base
    from src.database.dbConnectionHandler import DBConnHandler

    connHandler: DBConnHandler = DBConnHandler()

    Base.metadata.create_all(connHandler.get_engine())
    uvicorn.run(app, host='0.0.0.0', port=8000)
