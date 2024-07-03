from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class ContatoResponse(BaseModel):
    contatoId: int
    escritorioId: Optional[int]
    advogadoId: Optional[int]
    numero: int
    ehWatsapp: bool
    ehTelegram: bool
    principal: bool
    dataUltAlt: datetime
    dataCadastro: datetime

class ContatoRequest(BaseModel):
    escritorioId: Optional[int]
    advogadoId: Optional[int]
    numero: int
    ehWatsapp: bool
    ehTelegram: bool
    principal: bool
