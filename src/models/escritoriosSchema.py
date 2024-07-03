from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from src.models.enderecoSchema import EnderecoRequest


class EscritorioResponse(BaseModel):
    escritorioId: int
    nomeFantasia: str
    cnpj: Optional[str]
    telefone: str
    email: str
    inscEstadual: Optional[str]
    ativo: Optional[bool] = True
    dataUltAlt: Optional[datetime] = datetime.now()
    dataCadastro: Optional[datetime] = datetime.now()


class EscritorioRequest(BaseModel):
    nomeFantasia: str
    cnpj: Optional[str]
    telefone: str
    email: str
    inscEstadual: str


class EscritorioPostRequest(BaseModel):
    escritorio: EscritorioRequest
    endereco: EnderecoRequest
