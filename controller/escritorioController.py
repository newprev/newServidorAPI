from typing import List

from fastapi import APIRouter, HTTPException, status
from pymysql import IntegrityError
from sqlalchemy_utils import Choice

from models.escritoriosModel import Escritorio, EscritorioResponse, EscritorioPostRequest
from models.enderecoModel import Endereco
from repository.escritorioRep import EscritorioRepository
from utils.helpers import decideEstado

TAG_PREFIX = "/escritorio"
escritorioRouter = APIRouter(prefix=TAG_PREFIX, tags=[TAG_PREFIX])


@escritorioRouter.get('/all', response_model=List[EscritorioResponse], status_code=status.HTTP_200_OK)
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

@escritorioRouter.get('/{escritorioId}', response_model=EscritorioResponse, status_code=status.HTTP_200_OK)
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

@escritorioRouter.post('/', status_code=status.HTTP_201_CREATED)
def insereEscritorio(escritorioPost: EscritorioPostRequest):
    """
    Insere escritório por meio do modelo EscritorioPostRequest
    """
    enderecoModel = Endereco(
        endereco=escritorioPost.endereco,
        numero=escritorioPost.numero,
        cep=escritorioPost.cep,
        complemento=escritorioPost.complemento,
        cidade=escritorioPost.cidade,
        estado=decideEstado(escritorioPost.estado),
        bairro=escritorioPost.bairro
    )
    escritorioModel = Escritorio(
        nomeFantasia=escritorioPost.nomeFantasia,
        cnpj=escritorioPost.cnpj,
        telefone=escritorioPost.telefone,
        email=escritorioPost.email,
        inscEstadual=escritorioPost.inscEstadual
    )

    escritorioRepository: EscritorioRepository = EscritorioRepository()
    escritorioInserido: dict = escritorioRepository.insreNovoEscritorio(escritorioModel, enderecoModel)

    if not escritorioInserido:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível inserir o escritório"
        )

    return escritorioInserido

@escritorioRouter.delete('/{escritorioId}', status_code=status.HTTP_200_OK)
def deletaEscritorio(escritorioId: int) -> dict:
    """
    Deleta Escritorio dado escritorioId
    """

    escritorioRepository: EscritorioRepository = EscritorioRepository()
    escritorioIdDeletado: int = escritorioRepository.deletaEscritorioPorId(escritorioId)

    if not escritorioIdDeletado or escritorioIdDeletado == -1:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail="Escritório não deletado"
        )

    return {
        "escritorioIdDeletado": escritorioIdDeletado
    }
