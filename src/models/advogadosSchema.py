from datetime import datetime

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
    dataCadastro: datetime

class AdvogadoRequest(BaseModel):
    escritorioId: int
    primeiroNome: str
    sobrenome: str
    email: str
    numeroOAB: str
    cpf: str
    nacionalidade: str
    estadoCivil: str
