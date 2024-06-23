#SQLAlchemy primeiro
#Request e Responses em baixo

from datetime import datetime
from typing import Optional

from sqlalchemy import String, Column, Integer, Boolean, DateTime
from sqlalchemy_utils import EmailType

from src.database.database import Base
from src.utils.helpers import getEstados


class Escritorio(Base):
    __tablename__ = "Escritorio"

    ESTADO = getEstados()

    escritorioId = Column(Integer, primary_key=True, autoincrement=True)
    nomeFantasia = Column(String(50))
    cnpj = Column(String(14), nullable=True, unique=True)
    telefone = Column(String(11), nullable=True, unique=True)
    email = Column(EmailType, unique=True)
    inscEstadual = Column(String(9), nullable=True, unique=True)
    ativo = Column(Boolean, default=True)
    dataUltAlt = Column(DateTime, default=datetime.now(), nullable=False)
    dataCadastro = Column(DateTime, default=datetime.now(), nullable=False)

    def __str__(self):
        return self.username

    def toDict(self):
        return {
            "escritorioId": self.escritorioId,
            "nomeFantasia": self.nomeFantasia,
            "cnpj": self.cnpj,
            "telefone": self.telefone,
            "email": self.email,
            "inscEstadual": self.inscEstadual,
            "ativo": self.ativo,
            "dataUltAlt": f"{self.dataUltAlt}",
            "dataCadastro": f"{self.dataCadastro}"
        }


from pydantic import BaseModel
class EscritorioResponse(BaseModel):
    escritorioId: int
    nomeFantasia: str
    cnpj: Optional[str]
    telefone: str
    email: str
    inscEstadual: str
    ativo: bool
    dataUltAlt: datetime
    dataCadastro: datetime

class EscritorioRequest(BaseModel):
    nomeFantasia: str
    cnpj: Optional[str]
    telefone: str
    email: str
    inscEstadual: str

class EscritorioPostRequest(BaseModel):
    # Escritorio
    nomeFantasia: str
    cnpj: Optional[str]
    telefone: str
    email: str
    inscEstadual: str

    # Endereco
    endereco: str
    numero: int
    cep: str
    complemento: Optional[str]
    cidade: str
    estado: str
    bairro: str