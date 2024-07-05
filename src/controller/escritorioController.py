from pprint import pprint
from typing import List, Any

from fastapi import APIRouter, HTTPException, status

from src.models.erroSchema import NewPrevErro
from src.models.escritoriosModel import Escritorio
from src.models.enderecoModel import Endereco
from src.models.escritoriosSchema import EscritorioResponse, EscritorioPostRequest
from src.repository.escritorioRep import EscritorioRepository

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
    enderecoModel = Endereco(**escritorioPost.endereco.dict())
    escritorioModel = Escritorio(**escritorioPost.escritorio.dict())

    escritorioRepository: EscritorioRepository = EscritorioRepository()
    retornoRepo: Any[NewPrevErro, EscritorioPostRequest] = escritorioRepository.insreNovoEscritorio(escritorioModel, enderecoModel)

    print("\n1 ---------------- ")
    pprint(retornoRepo.dict())
    print("2 ----------------\n\n ")

    if isinstance(retornoRepo, EscritorioPostRequest):
        return retornoRepo

    if retornoRepo.observacao is not None and 'Chave duplicada' in retornoRepo.observacao:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Advogado não pôde ser cadastrado"
        )

    if isinstance(retornoRepo.erro, KeyError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Informacao errada: {retornoRepo.erro}"
        )

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


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
