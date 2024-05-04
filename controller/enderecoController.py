from typing import List

from fastapi import APIRouter, HTTPException
from models.enderecoModel import Endereco, EnderecoRequest, EnderecoResponse
from repository.enderecoRep import EnderecoRepository

TAG_PREFIX = "/endereco"
enderecoRouter = APIRouter(prefix=TAG_PREFIX, tags=[TAG_PREFIX])


@enderecoRouter.get('/all', response_model=List[EnderecoResponse], status_code=200)
def buscaTodos() -> List[EnderecoRequest]:
    """
    Retorna todos os enderecos cadastrados no banco
    """
    enderecoRepository: EnderecoRepository = EnderecoRepository()
    listaAllEnderecos: List[Endereco]
    listaAllResponse: List[EnderecoResponse]

    listaAllEnderecos = enderecoRepository.selectAll()
    if listaAllEnderecos is None:
        raise HTTPException(status_code=404, detail='Nenhum endereço encontrado')
    listaAllResponse = [EnderecoResponse(**endereco.toDict()) for endereco in listaAllEnderecos]

    return listaAllResponse


@enderecoRouter.get('/{enderecoId}', response_model=EnderecoResponse, status_code=200)
def buscaEnderecoPorId(enderecoId: int) -> EnderecoResponse:
    """
    Retorna endereco cadastrado no banco, dado enderecoId
    """
    enderecoRepository: EnderecoRepository = EnderecoRepository()
    enderecoBuscado: Endereco = enderecoRepository.buscaEnderecoPorId(enderecoId)
    if enderecoBuscado is None:
        raise HTTPException(status_code=404, detail='Nenhum endereço encontrado')
    enderecoResponse = EnderecoResponse(**enderecoBuscado.toDict())

    return enderecoResponse

@enderecoRouter.get('/escritorio/{escritorioId}', response_model=List[EnderecoResponse], status_code=200)
def buscaEnderecoPorEscritorioId(escritorioId: int) -> List[EnderecoResponse]:
    """
    Retorna endereco cadastrado no banco, dado escritorioId
    """
    enderecoRepository: EnderecoRepository = EnderecoRepository()
    listaEnderecosBuscados: List[Endereco] = enderecoRepository.buscaPorEscritorioId(escritorioId)
    if listaEnderecosBuscados is None:
        raise HTTPException(status_code=404, detail='Nenhum endereço encontrado')
    listaEnderecosResponse = [EnderecoResponse(**endereco.toDict()) for endereco in listaEnderecosBuscados]

    return listaEnderecosResponse

@enderecoRouter.get('/advogado/{advogadoId}', response_model=List[EnderecoResponse], status_code=200)
def buscaEnderecoPorAdvogadoId(advogadoId: int) -> List[EnderecoResponse]:
    """
    Retorna endereco cadastrado no banco, dado advogadoId
    """
    enderecoRepository: EnderecoRepository = EnderecoRepository()
    listaEnderecosBuscados: List[Endereco] = enderecoRepository.buscaPorAdvogadoId(advogadoId)
    if listaEnderecosBuscados is None:
        raise HTTPException(status_code=404, detail='Nenhum endereço encontrado')
    listaEnderecosResponse = [EnderecoResponse(**endereco.toDict()) for endereco in listaEnderecosBuscados]

    return listaEnderecosResponse
