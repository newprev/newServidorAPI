#SQLAlchemy primeiro
#Request e Responses em baixo

from datetime import datetime
from typing import Optional

from sqlalchemy import String, Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy_utils import ChoiceType

from database.database import Base
from utils.helpers import getEstados


class Endereco(Base):
    __tablename__ = "Endereco"

    ESTADO = getEstados()

    enderecoId = Column(Integer, primary_key=True, autoincrement=True)
    escritorioId = Column(Integer, ForeignKey("Escritorio.escritorioId"))
    advogadoId = Column(Integer, ForeignKey("Advogados.advogadoId"))
    endereco = Column(String(80))
    numero = Column(Integer, nullable=True)
    cep = Column(String(8))
    complemento = Column(String(50))
    cidade = Column(String(30))
    estado = Column(ChoiceType(ESTADO), nullable=False, default='SP')
    bairro = Column(String(50))
    ativo = Column(Boolean, default=True)
    dataUltAlt = Column(DateTime, default=datetime.now(), nullable=False)
    dataCadastro = Column(DateTime, default=datetime.now(), nullable=False)

    def __str__(self):
        return f"{self.endereco} - {self.numero}  {self.cidade}/{self.estado.code}"

    def toDict(self):
        return {
            "enderecoId": self.enderecoId,
            "escritorioId": self.escritorioId,
            "advogadoId": self.advogadoId,
            "endereco": self.endereco,
            "numero": self.numero,
            "cep": self.cep,
            "complemento": self.complemento,
            "cidade": self.cidade,
            "estado": self.estado.code,
            "bairro": self.bairro,
            "ativo": self.ativo,
            "dataUltAlt": f"{self.dataUltAlt}",
            "dataCadastro": f"{self.dataCadastro}"
        }


from pydantic import BaseModel
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