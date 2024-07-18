from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class AdvogadoResponse(BaseModel):
    advogadoId: int
    primeiroNome: str
    sobrenome: str
    email: str
    numeroOAB: str
    cpf: str
    nacionalidade: str
    estadoCivil: str
    admin: bool
    ativo: bool
    confirmado: bool
    dataUltAlt: datetime
    dataCadastro: Optional[datetime] = None

class AdvogadoRequest(BaseModel):
    escritorioId: int
    primeiroNome: str
    sobrenome: str
    email: str
    numeroOAB: str
    cpf: str
    nacionalidade: str
    estadoCivil: str
    admin: Optional[bool] = None
    ativo: Optional[bool] = None
    confirmado: Optional[bool] = None
