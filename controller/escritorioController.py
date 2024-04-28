from typing import List

from fastapi import APIRouter
from models.escritoriosModel import Escritorio, EscritorioResponse
from repository.escritorioRep import EscritorioRepository

TAG_PREFIX = "/escritorio"
escritorioRouter = APIRouter(prefix=TAG_PREFIX, tags=[TAG_PREFIX])


@escritorioRouter.get('/all', response_model=List[EscritorioResponse], status_code=200)
def buscaTodos() -> List[EscritorioResponse]:
    """
    Retorna todos os advogados cadastrados no banco
    """
    escritorioRepository: EscritorioRepository = EscritorioRepository()
    listaAllEscritorios: List[Escritorio]
    listaAllResponse: List[EscritorioResponse]

    listaAllEscritorios = escritorioRepository.selectAll()
    print(f"{listaAllEscritorios[0].toDict()=}")
    listaAllResponse = [EscritorioResponse(**escritorio.toDict()) for escritorio in listaAllEscritorios]

    return listaAllResponse

