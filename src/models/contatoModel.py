#SQLAlchemy primeiro
#Request e Responses em baixo

from datetime import datetime
from sqlalchemy import ForeignKey, Column, Integer, BigInteger, Boolean, DateTime
from typing import Optional

from src.database.database import Base


class Contato(Base):
    __tablename__ = "Contato"

    contatoId = Column(Integer, primary_key=True, autoincrement=True)
    escritorioId = Column(Integer, ForeignKey("Escritorio.escritorioId", ondelete='CASCADE'))
    advogadoId = Column(Integer, ForeignKey("Advogado.advogadoId", ondelete='CASCADE'))
    numero = Column(BigInteger, unique=True, nullable=False)
    ehWatsapp = Column(Boolean, default=True, nullable=False)
    ehTelegram = Column(Boolean, default=True, nullable=False)
    principal = Column(Boolean, default=True, nullable=False)
    dataUltAlt = Column(DateTime, default=datetime.now, nullable=False)
    dataCadastro = Column(DateTime, default=datetime.now, nullable=False)

    def toDict(self):
        return {
            "contatoId": self.contatoId,
            "escritorioId": self.escritorioId,
            "advogadoId": self.advogadoId,
            "numero": self.numero,
            "ehWatsapp": self.ehWatsapp,
            "ehTelegram": self.ehTelegram,
            "principal": self.principal,
            "dataUltAlt": self.dataUltAlt,
            "dataCadastro": self.dataCadastro
        }


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
