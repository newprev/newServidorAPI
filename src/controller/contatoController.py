from typing import List

from fastapi import APIRouter, HTTPException
from src.models.contatoModel import Contato, ContatoResponse, ContatoRequest
from src.repository.contatoRep import ContatoRepository

TAG_PREFIX = "/contato"
contatoRouter = APIRouter(prefix=TAG_PREFIX, tags=[TAG_PREFIX])


@contatoRouter.get('/all', response_model=List[ContatoResponse], status_code=200)
def buscaTodos() -> List[ContatoRequest]:
    """
    Retorna todos os contatos cadastrados no banco
    """
    contatoRepository: ContatoRepository = ContatoRepository()
    listaAllContatos: List[Contato]
    listaAllResponse: List[ContatoResponse]

    listaAllContatos = contatoRepository.selectAll()
    if listaAllContatos is None:
        raise HTTPException(status_code=404, detail='Nenhum contato encontrado')
    listaAllResponse = [ContatoResponse(**contato.toDict()) for contato in listaAllContatos]

    return listaAllResponse


@contatoRouter.get('/{contatoId}', response_model=ContatoResponse, status_code=200)
def buscaContatoPorId(contatoId: int) -> ContatoResponse:
    """
    Retorna contato cadastrado no banco, dado contatoId
    """
    contatoRepository: ContatoRepository = ContatoRepository()
    contatoBuscado: Contato = contatoRepository.buscaContatoPorId(contatoId)
    if contatoBuscado is None:
        raise HTTPException(status_code=404, detail='Nenhum contato encontrado')
    contatoResponse = ContatoResponse(**contatoBuscado.toDict())

    return contatoResponse

@contatoRouter.get('/escritorio/{escritorioId}', response_model=List[ContatoResponse], status_code=200)
def buscaContatoPorEscritorioId(escritorioId: int) -> List[ContatoResponse]:
    """
    Retorna contato cadastrado no banco, dado escritorioId
    """
    contatoRepository: ContatoRepository = ContatoRepository()
    listaContatosBuscados: List[Contato] = contatoRepository.buscaPorEscritorioId(escritorioId)
    if listaContatosBuscados is None:
        raise HTTPException(status_code=404, detail='Nenhum contato encontrado')
    listaContatosResponse = [ContatoResponse(**contato.toDict()) for contato in listaContatosBuscados]

    return listaContatosResponse

@contatoRouter.get('/advogado/{advogadoId}', response_model=List[ContatoResponse], status_code=200)
def buscaContatoPorAdvogadoId(advogadoId: int) -> List[ContatoResponse]:
    """
    Retorna contato cadastrado no banco, dado advogadoId
    """
    contatoRepository: ContatoRepository = ContatoRepository()
    listaContatosBuscados: List[Contato] = contatoRepository.buscaPorAdvogadoId(advogadoId)
    if listaContatosBuscados is None:
        raise HTTPException(status_code=404, detail='Nenhum contato encontrado')
    listaContatosResponse = [ContatoResponse(**contato.toDict()) for contato in listaContatosBuscados]

    return listaContatosResponse
