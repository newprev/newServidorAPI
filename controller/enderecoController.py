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
    try:
        enderecoRepository: EnderecoRepository = EnderecoRepository()
        listaAllEnderecos: List[Endereco]
        listaAllResponse: List[EnderecoResponse]

        listaAllEnderecos = enderecoRepository.selectAll()
        if listaAllEnderecos is None:
            raise HTTPException(status_code=404, detail='Nenhum escritório encontrado')
        listaAllResponse = [EnderecoResponse(**endereco.toDict()) for endereco in listaAllEnderecos]

        return listaAllResponse

    except Exception as err:
        return err

@enderecoRouter.get('/{enderecoId}', response_model=EnderecoResponse, status_code=200)
def buscaEnderecoPorId(enderecoId: int) -> EnderecoResponse:
    """
    Retorna endereco cadastrado no banco, dado enderecoId
    """
    enderecoRepository: EnderecoRepository = EnderecoRepository()
    enderecoBuscado: Endereco = enderecoRepository.buscaEnderecoPorId(enderecoId)
    if enderecoBuscado is None:
        raise HTTPException(status_code=404, detail='Nenhum escritório encontrado')
    enderecoResponse = EnderecoResponse(**enderecoBuscado.toDict())

    return enderecoResponse
