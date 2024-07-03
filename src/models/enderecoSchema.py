from datetime import datetime
from pprint import pprint
from typing import Optional, List

from pydantic import BaseModel, field_validator

from src.utils.helpers import getEstadosDict


class EnderecoResponse(BaseModel):
    enderecoId: int
    escritorioId: Optional[int]
    advogadoId: Optional[int]
    endereco: str
    numero: int
    cep: str
    complemento: Optional[str]
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
    complemento: Optional[str]
    cidade: str
    estado: str
    bairro: str

    @field_validator('estado')
    def validaEstado(cls, v):
        listaNome = getEstadosDict().keys()
        listaSiglas = getEstadosDict().values()

        print(f"{v} ___________________________")
        print(f"{listaNome=}")
        print(f"{listaSiglas=}")
        print(f"{v not in listaEstados=}")
        print("___________________________")

        if v in listaSiglas:
            return v

        if v not in listaEstados:
            raise ValueError("Estado não encontrado")
        return v
