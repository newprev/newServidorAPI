from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from src.models.enderecoSchema import EnderecoRequest


class EscritorioResponse(BaseModel):
    escritorioId: Optional[int] = None
    nomeEscritorio: str
    nomeFantasia: str
    cnpj: Optional[str] = None
    telefone: str
    email: str
    inscEstadual: Optional[str] = None
    ativo: Optional[bool] = True
    dataUltAlt: Optional[datetime] = datetime.now()
    dataCadastro: Optional[datetime] = datetime.now()


class EscritorioRequest(BaseModel):
    escritorioId: Optional[int] = None
    nomeEscritorio: str
    nomeFantasia: str
    cnpj: Optional[str] = None
    telefone: str
    email: str
    inscEstadual: Optional[str] = None


class EscritorioPostRequest(BaseModel):
    escritorio: EscritorioRequest
    endereco: EnderecoRequest


class EscritorioCliente(BaseModel):
    escritorioId: int
    bairro: str
    cep: str
    cidade: str
    cnpj: str
    complemento: Optional[str] = None
    email: EmailStr
    endereco: str
    estado: str
    inscEstadual: Optional[str] = None
    nomeEscritorio: str
    nomeFantasia: str
    numero: int
    telefone: str
    dataCadastro: Optional[datetime] = datetime.now()
    dataUltAlt: Optional[datetime] = datetime.now()
