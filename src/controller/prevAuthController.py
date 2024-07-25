from datetime import timezone
from random import randint
from typing import List

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, HTTPException, status

from src.models.advogadosModel import Advogado
from src.models.advogadosSchema import AdvogadoResponse
from src.models.emailModel import EmailModel
from src.models.prevAuthModel import PrevAuth
from src.models.prevAuthSchema import AuthResponse, PrimeiroAcessoEsqueceuSenha, CodAcessoSchema
from src.models.trocaSenhaModel import TrocaSenha
from src.models.trocaSenhaSchema import TrocaSenhaSchema
from src.repository.prevAuthRep import PrevAuthRepository
from src.utils.enums.authEnums import EsqueceuSenhaPAcesso
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

        listaAllPrevAuth = prevAuthRepository.selectAll()
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
@prevAuthRouter.post('/advogado/trocaSenha/', status_code=status.HTTP_201_CREATED)
def trocaSenhaAdvogado(infoPrimeiroAcesso: PrimeiroAcessoEsqueceuSenha) -> dict:
    """
    Insere informação de troca de senha
    """
    infoRecebida: PrimeiroAcessoEsqueceuSenha = PrimeiroAcessoEsqueceuSenha(**infoPrimeiroAcesso.model_dump())
    if len(infoRecebida.info) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verifique se as informações enviadas estão corretas"
        )

    cpfEnviado = validaCpf(infoRecebida.info)
    emailEnviado = validaEmail(infoRecebida.info)
    if not cpfEnviado and not emailEnviado:
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

    emailModel: EmailModel = EmailModel(
        adv=AdvogadoResponse(**advogado.toDict())
    )

    if infoRecebida.esqueceuSenha:
        trocaSenha.tipoTroca = EsqueceuSenhaPAcesso.esqueceuSenha
        advogado.confirmado = True
        emailModel.sendAlteracaoAdvogado()

    else:
        advogado.confirmado = False
        trocaSenha.tipoTroca = EsqueceuSenhaPAcesso.primeiroAcesso
        emailModel.sendPrimeiroAcesso(trocaSenha)

    response: TrocaSenhaSchema = prevAuthRep.salvaAdvogadoTrocaSenha(advogado.advogadoId, trocaSenha)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verifique se as informações enviadas estão corretas"
        )

    return {"advogadoId": response.advogadoId}


@prevAuthRouter.patch('/advogado/autenticaCodAcesso/', status_code=status.HTTP_200_OK)
def autenticaCodAcesso(infoCodAcesso: CodAcessoSchema):
    """
    Verifica código enviado do primeiro acesso
    """
    try:
        print(f"\ninfoCodAcesso: {infoCodAcesso.model_dump()=}\n")
        prevAuthRep: PrevAuthRepository = PrevAuthRepository()
        codigoAcessoConfirmado: bool = prevAuthRep.buscaConfirmaCodPrimeiroAcesso(infoCodAcesso)
        if codigoAcessoConfirmado:
            return HTTPException(status_code=status.HTTP_200_OK, detail="Código de acesso confirmado.")
        else:
            return HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="Chave incorreta")

    except Exception as err:
        print(f'auth/advogado/autenticaCodAcesso/ - err: {err}')
        return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

