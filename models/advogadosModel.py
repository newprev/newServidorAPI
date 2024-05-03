#SQLAlchemy primeiro
#Request e Responses em baixo

from datetime import datetime
from sqlalchemy import ForeignKey, String, Column, Integer, Boolean, DateTime
from sqlalchemy_utils import EmailType, PasswordType

from database.database import Base

SCHEMES = [
    'pbkdf2_sha512',
    'md5_crypt'
]

class Advogado(Base):
    __tablename__ = "Advogados"

    advogadoId = Column(Integer, primary_key=True, autoincrement=True)
    escritorioId = Column(Integer, ForeignKey("Escritorio.escritorioId"))
    primeiroNome = Column(String(20), nullable=False)
    sobrenome = Column(String(40), nullable=False)
    email = Column(EmailType, nullable=False, unique=True)
    senha = Column(PasswordType(schemes=SCHEMES), nullable=False)
    numeroOAB = Column(String(9), nullable=False, unique=True)
    cpf = Column(String(11), nullable=False, unique=True)
    nacionalidade = Column(String(40), default='brasileiro', nullable=False)
    estadoCivil = Column(String(20), default='solteiro', nullable=False)
    admin = Column(Boolean, default=False)
    ativo = Column(Boolean, default=True)
    confirmado = Column(Boolean, default=False)
    dataUltAlt = Column(DateTime, default=datetime.now, nullable=False)
    dataCadastro = Column(DateTime, default=datetime.now, nullable=False)

    def __str__(self):
        return f"id: {self.advogadoId}, nome: {self.primeiroNome}, email: {self.email}, OAB: {self.numeroOAB}"

    def toDict(self, enviaEscritorio: bool = True):
        return {
            "advogadoId": self.advogadoId,
            # "escritorioId": self.escritorioId.toDict() if enviaEscritorio else self.escritorioId.escritorioId,
            "primeiroNome": self.primeiroNome,
            "sobrenome": self.sobrenome,
            "email": self.email,
            "senha": self.senha,
            "numeroOAB": self.numeroOAB,
            "cpf": self.cpf,
            "nacionalidade": self.nacionalidade,
            "estadoCivil": self.estadoCivil,
            "admin": self.admin,
            "ativo": self.ativo,
            "confirmado": self.confirmado,
            # "fotoPath": self.fotoPath,
            "dataUltAlt": self.dataUltAlt,
            "dataCadastro": self.dataCadastro
        }


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