from pprint import pprint
from random import randint
from typing import List

from fastapi import APIRouter, HTTPException, status

from src.models.advogadosModel import Advogado
from src.models.prevAuth import PrevAuth, AuthResponse, PrimeiroAcessoEsqueceuSenha
from src.models.trocaSenhaModel import TrocaSenha, TrocaSenhaSchema
from src.repository.prevAuthRep import PrevAuthRepository
from src.utils.enums.authEnums import EsqueceuSenhaPAcesso
from src.utils.enums.loginEnums import TipoTrocaSenha
from src.utils.validators import validaCpf, validaEmail

TAG_PREFIX = "/auth"
prevAuthRouter = APIRouter(prefix=TAG_PREFIX, tags=[TAG_PREFIX])


@prevAuthRouter.get('/all', response_model=List[AuthResponse], status_code=status.HTTP_200_OK)
def buscaTodos() -> List[AuthResponse]:
    """
    Retorna toda as autenticacoes cadastrados no banco
    """
    try:
        prevAuthRepository: PrevAuthRepository = PrevAuthRepository()
        listaAllPrevAuth: List[PrevAuth]
        listaAllResponse: List[AuthResponse]

        listaAllPrevAuth = PrevAuthRepository.selectAll()
        if listaAllPrevAuth is None:
            raise HTTPException(status_code=404, detail='Nenhuma autenticacao encontrada')
        listaAllResponse = [AuthResponse(**auth.toDict()) for auth in listaAllPrevAuth]

        return listaAllResponse
    except Exception as err:
        return err

# @escritorioRouter.get('/{escritorioId}', response_model=EscritorioResponse, status_code=status.HTTP_200_OK)
# def buscaEscritorioPorId(escritorioId: int) -> EscritorioResponse:
#     """
#     Retorna todos os advogados cadastrados no banco
#     """
#     escritorioRepository: EscritorioRepository = EscritorioRepository()
#     escritorioBuscado: Escritorio = escritorioRepository.buscaEscritorioPorId(escritorioId)
#     if escritorioBuscado is None:
#         raise HTTPException(status_code=404, detail='Nenhum escritório encontrado')
#     escritorioResponse = EscritorioResponse(**escritorioBuscado.toDict())
#
#     return escritorioResponse
#
@prevAuthRouter.post('/advogados/trocaSenha/', status_code=status.HTTP_201_CREATED)
def trocaSenhaAdvogado(infoPrimeiroAcesso: PrimeiroAcessoEsqueceuSenha) -> dict:
    """
    Insere informação de troca de senha
    """
    infoRecebida: PrimeiroAcessoEsqueceuSenha = PrimeiroAcessoEsqueceuSenha(**infoPrimeiroAcesso.dict())
    if len(infoRecebida.info) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verifique se as informações enviadas estão corretas"
        )

    cpfEnviado = validaCpf(infoRecebida.info)
    emailEnviado = validaEmail(infoRecebida.info)
    if not (cpfEnviado or emailEnviado):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verifique se as informações enviadas estão corretas"
        )

    prevAuthRep: PrevAuthRepository = PrevAuthRepository()
    if cpfEnviado and not emailEnviado:
        advogado: Advogado = prevAuthRep.buscaAdvogadoPorCPF(infoRecebida.info)
    if emailEnviado and not cpfEnviado:
        advogado: Advogado = prevAuthRep.buscaAdvogadoPorEmail(infoRecebida.info)

    if advogado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Verifique se as informações enviadas estão corretas"
        )

    trocaSenha: TrocaSenha = TrocaSenha()
    trocaSenha.advogadoId = advogado.advogadoId
    trocaSenha.primAcesso = not infoRecebida.esqueceuSenha
    trocaSenha.codAcesso = randint(10000, 99999)

    if infoRecebida.esqueceuSenha:
        trocaSenha.tipoTroca = EsqueceuSenhaPAcesso.esqueceuSenha
        advogado.confirmado = True
        # trocouSenhaAdvogado(advogado, trocaSenha) Deve enviar email para o advogado
    else:
        advogado.confirmado = False
        trocaSenha.tipoTroca = EsqueceuSenhaPAcesso.primeiroAcesso
        # primeiroAcessoAdvogado(advogado, trocaSenha) Deve enviar email para o advogado cadastrado

    response: TrocaSenhaSchema = prevAuthRep.salvaAdvogadoTrocaSenha(advogado.advogadoId, trocaSenha)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verifique se as informações enviadas estão corretas"
        )

    return {"advogadoId": response.advogadoId}
#
# @escritorioRouter.delete('/{escritorioId}', status_code=status.HTTP_200_OK)
# def deletaEscritorio(escritorioId: int) -> dict:
#     """
#     Deleta Escritorio dado escritorioId
#     """
#
#     escritorioRepository: EscritorioRepository = EscritorioRepository()
#     escritorioIdDeletado: int = escritorioRepository.deletaEscritorioPorId(escritorioId)
#
#     if not escritorioIdDeletado or escritorioIdDeletado == -1:
#         raise HTTPException(
#             status_code=status.HTTP_304_NOT_MODIFIED,
#             detail="Escritório não deletado"
#         )
#
#     return {
#         "escritorioIdDeletado": escritorioIdDeletado
#     }
