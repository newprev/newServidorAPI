from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from enum import Enum


class AuthResponse(BaseModel):
    authId: int
    tipoAuth: Enum
    escritorioId: int
    advogadoId: int
    authDeOnde: Enum
    horaAuth: datetime
    dataCadastro: datetime


class AuthRequest(BaseModel):
    authId: Optional[int]
    tipoAuth: Enum
    escritorioId: Optional[int]
    advogadoId: Optional[int]
    horaAuth: datetime
    authDeOnde: Enum


class PrimeiroAcessoEsqueceuSenha(BaseModel):
    info: str
    esqueceuSenha: bool


class CodAcessoSchema(BaseModel):
    escritorioId: int
    advogadoId: Optional[int] = None
    codigo: int

