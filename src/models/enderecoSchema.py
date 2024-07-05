from datetime import datetime
from pprint import pprint
from typing import Optional, List

from pydantic import BaseModel, field_validator
from sqlalchemy_utils import Choice

from src.utils.helpers import getEstadosDict


class EnderecoResponse(BaseModel):
    enderecoId: int
    escritorioId: Optional[int]
    advogadoId: Optional[int]
    endereco: str
    numero: int
    cep: str
    complemento: Optional[str] = None
    cidade: str
    estado: str
    bairro: str
    ativo: bool
    dataUltAlt: datetime
    dataCadastro: datetime


class EnderecoRequest(BaseModel):
    endereco: str
    numero: int
    cep: str
    complemento: Optional[str] = None
    cidade: str
    estado: str
    bairro: str

    @field_validator('estado')
    def validaEstado(cls, v):
        for sigla, nome in getEstadosDict().items():
            if v == sigla or v == nome:
                print(f"{sigla=}")
                return sigla

        raise ValueError("Estado não encontrado")
        return v
