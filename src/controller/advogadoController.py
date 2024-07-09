from random import randint
from typing import List

from fastapi import APIRouter, HTTPException, status
from src.models.advogadosModel import Advogado
from src.models.advogadosSchema import AdvogadoResponse, AdvogadoRequest
from src.models.emailModel import EmailModel
from src.models.escritoriosModel import Escritorio
from src.repository.advogadoRep import AdvogadoRepository
from src.repository.escritorioRep import EscritorioRepository

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
    if listaAllAdv is None:
        raise HTTPException(status_code=404, detail='Nenhum advogado foi encontrado')
    listaAllResponse = [AdvogadoResponse(**adv.toDict()) for adv in listaAllAdv]

    return listaAllResponse

@advogadoRouter.get('/{advogadoId}', response_model=AdvogadoResponse, status_code=200)
def buscaPorAdvogadoPorId(advogadoId: int) -> AdvogadoResponse:
    """
    Busca o advogado dado Id
    """
    advRepository: AdvogadoRepository = AdvogadoRepository()
    advogadoProcurado: Advogado = advRepository.buscaPorId(advogadoId)
    if advogadoProcurado is None:
        raise HTTPException(status_code=404, detail='Advogado não encontrado')

    return advogadoProcurado

@advogadoRouter.post('/', status_code=status.HTTP_201_CREATED)
def insereAdvogado(advogadoEnviado: AdvogadoRequest) -> AdvogadoResponse:
    """
    Insere advogado enviado e envia email
    """
    novoAdvogado: Advogado = Advogado(**advogadoEnviado.model_dump())
    if novoAdvogado.escritorioId is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Escritorio não encontrado"
        )

    escritorioRep: EscritorioRepository = EscritorioRepository()
    escritorioAtual: Escritorio = escritorioRep.buscaEscritorioPorId(novoAdvogado.escritorioId)

    if escritorioAtual is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Escritorio não encontrado"
        )

    advogadoRepository: AdvogadoRepository = AdvogadoRepository()
    novoAdvogado = advogadoRepository.insereNovoAdvogado(novoAdvogado)

    if not novoAdvogado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível inserir o advogado"
        )

    emailModel: EmailModel = EmailModel(adv=novoAdvogado, escritorio=escritorioAtual)
    emailModel.sendBoasVindasAdvogado()

    return AdvogadoResponse(**novoAdvogado.toDict())

