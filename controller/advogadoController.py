from typing import List

from fastapi import APIRouter
from models.advogadosModel import AdvogadoResponse, Advogado
from repository.advogadoRep import AdvogadoRepository

TAG_PREFIX = "/advogado"
advogadoRouter = APIRouter(prefix=TAG_PREFIX, tags=[TAG_PREFIX])


@advogadoRouter.get('/all', response_model=List[AdvogadoResponse], status_code=200)
def buscaTodos() -> List[AdvogadoResponse]:
    """
    Retorna todos os advogados cadastrados no banco
    """
    advRepository: AdvogadoRepository = AdvogadoRepository()
    listaAllAdv: List[Advogado]
    listaAllResponse: List[AdvogadoResponse]

    listaAllAdv = advRepository.selectAll()
    listaAllResponse = [AdvogadoResponse(**adv.toDict()) for adv in listaAllAdv]

    return listaAllResponse

