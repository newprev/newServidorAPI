from random import randint
from typing import List

from fastapi import APIRouter, HTTPException, status
from src.models.advogadosModel import AdvogadoResponse, AdvogadoRequest, Advogado
from src.repository.advogadoRep import AdvogadoRepository

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
    Insere advogado enviado
    """
    novoAdvogado = Advogado(
        primeiroNome=advogadoEnviado.primeiroNome,
        sobrenome=advogadoEnviado.sobrenome,
        email=advogadoEnviado.email,
        numeroOAB=advogadoEnviado.numeroOAB,
        cpf=advogadoEnviado.cpf,
        nacionalidade=advogadoEnviado.nacionalidade,
        estadoCivil=advogadoEnviado.estadoCivil,
        senha=f"{randint(1000, 9999)}",
        admin=False,
        ativo=True,
        confirmado=False
    )
    advogadoRepository: AdvogadoRepository = AdvogadoRepository()
    novoAdvogado = advogadoRepository.insereNovoAdvogado(novoAdvogado)

    if not novoAdvogado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível inserir o advogado"
        )


    return AdvogadoResponse(**novoAdvogado.toDict())

