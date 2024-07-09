from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from src.models.enderecoSchema import EnderecoRequest


class EscritorioResponse(BaseModel):
    escritorioId: Optional[int] = None
    nomeFantasia: str
    cnpj: Optional[str] = None
    telefone: str
    email: str
    inscEstadual: Optional[str] = None
    ativo: Optional[bool] = True
    dataUltAlt: Optional[datetime] = datetime.now()
    dataCadastro: Optional[datetime] = datetime.now()


class EscritorioRequest(BaseModel):
    nomeFantasia: str
    cnpj: Optional[str] = None
    telefone: str
    email: str
    inscEstadual: Optional[str] = None


class EscritorioPostRequest(BaseModel):
    escritorio: EscritorioRequest
    endereco: EnderecoRequest
