#SQLAlchemy primeiro
#Request e Responses em baixo

from datetime import datetime
from sqlalchemy import String, Column, Integer, Boolean, DateTime
from sqlalchemy_utils import EmailType, ChoiceType

from database.database import Base
from utils.helpers import getEstados


class Escritorio(Base):
    __tablename__ = "Escritorio"

    ESTADO = getEstados()

    escritorioId = Column(Integer, primary_key=True, autoincrement=True)
    nomeFantasia = Column(String(50))
    cnpj = Column(String(14), nullable=True, unique=True)
    telefone = Column(String(11), nullable=True, unique=True)
    email = Column(EmailType, unique=True)
    inscEstadual = Column(String(9), nullable=True, unique=True)
    endereco = Column(String(80))
    numero = Column(Integer, nullable=True)
    cep = Column(String(8))
    complemento = Column(String(50))
    cidade = Column(String(30))
    estado = Column(ChoiceType(ESTADO), nullable=False, default='SP')
    bairro = Column(String(50))
    ativo = Column(Boolean, default=True)
    # logoPath = models.ImageField(upload_to='logo/%Y/%m')
    dataUltAlt = Column(DateTime, default=datetime.now(), nullable=False)
    dataCadastro = Column(DateTime, default=datetime.now(), nullable=False)

    def get_nomeFantasia(self):
        return self.nomeFantasia

    def __str__(self):
        return self.username

    def retEmail(self):
        return self.email

    def toDict(self):
        return {
            "escritorioId": self.escritorioId,
            "nomeFantasia": self.nomeFantasia,
            "cnpj": self.cnpj,
            "telefone": self.telefone,
            "email": self.email,
            "inscEstadual": self.inscEstadual,
            "endereco": self.endereco,
            "numero": self.numero,
            "cep": self.cep,
            "complemento": self.complemento,
            "cidade": self.cidade,
            "estado": self.estado.value,
            "bairro": self.bairro,
            "ativo": self.ativo,
            "dataUltAlt": f"{self.dataUltAlt}",
            "dataCadastro": f"{self.dataCadastro}"
        }


from pydantic import BaseModel
class EscritorioResponse(BaseModel):
    escritorioId: int
    nomeFantasia: str
    cnpj: str
    telefone: str
    email: str
    inscEstadual: str
    endereco: str
    numero: int
    cep: str
    complemento: str
    cidade: str
    estado: str
    bairro: str
    ativo: bool
    dataUltAlt: datetime
    dataCadastro: datetime