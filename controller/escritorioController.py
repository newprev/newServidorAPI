from typing import List

from fastapi import APIRouter, HTTPException
from models.escritoriosModel import Escritorio, EscritorioResponse
from repository.escritorioRep import EscritorioRepository

TAG_PREFIX = "/escritorio"
escritorioRouter = APIRouter(prefix=TAG_PREFIX, tags=[TAG_PREFIX])


@escritorioRouter.get('/all', response_model=List[EscritorioResponse], status_code=200)
def buscaTodos() -> List[EscritorioResponse]:
    """
    Retorna todos os advogados cadastrados no banco
    """
    try:
        escritorioRepository: EscritorioRepository = EscritorioRepository()
        listaAllEscritorios: List[Escritorio]
        listaAllResponse: List[EscritorioResponse]

        listaAllEscritorios = escritorioRepository.selectAll()
        if listaAllEscritorios is None:
            raise HTTPException(status_code=404, detail='Nenhum escritório encontrado')
        listaAllResponse = [EscritorioResponse(**escritorio.toDict()) for escritorio in listaAllEscritorios]

        return listaAllResponse
    except Exception as err:
        return err

@escritorioRouter.get('/{escritorioId}', response_model=EscritorioResponse, status_code=200)
def buscaEscritorioPorId(escritorioId: int) -> EscritorioResponse:
    """
    Retorna todos os advogados cadastrados no banco
    """
    escritorioRepository: EscritorioRepository = EscritorioRepository()
    escritorioBuscado: Escritorio = escritorioRepository.buscaEscritorioPorId(escritorioId)
    if escritorioBuscado is None:
        raise HTTPException(status_code=404, detail='Nenhum escritório encontrado')
    escritorioResponse = EscritorioResponse(**escritorioBuscado.toDict())

    return escritorioResponse

@escritorioRouter.post('/escritorio', response_model=EscritorioResponse, status_code=201)
def insereEscritorio() -> EscritorioResponse:
    """
    Insere escritório
    """
    try:
        pass
    except Exception as err:
        return err

