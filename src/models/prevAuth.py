#SQLAlchemy primeiro
#Request e Responses em baixo

from datetime import datetime
from typing import Optional
import enum

from src.utils.enums.authEnums import AuthDeOnde, TipoAuth

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum

from src.database.database import Base


class PrevAuth(Base):
    __tablename__ = "PrevAuth"

    authId = Column(Integer, primary_key=True, autoincrement=True)
    tipoAuth = Column(Enum(TipoAuth, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    escritorioId = Column(Integer, ForeignKey("Escritorio.escritorioId"), nullable=True)
    advogadoId = Column(Integer, ForeignKey("Advogado.advogadoId"), nullable=True)
    authDeOnde = Column(Enum(AuthDeOnde, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    horaAuth = Column(DateTime, default=datetime.now(), nullable=False)
    dataCadastro = Column(DateTime, default=datetime.now(), nullable=False)

    def __str__(self):
        return f"{self.authId} - {self.tipoAuth}: {self.escritorioId=}/{self.advogadoId=}\n{self.dataCadastro}"

    def toDict(self):
        return {
            "authId": self.authId,
            "tipoAuth": self.tipoAuth,
            "escritorioId": self.escritorioId,
            "advogadoId": self.advogadoId,
            "authDeOnde": self.authDeOnde,
            "horaAuth": self.horaAuth,
            "dataCadastro": self.dataCadastro
        }


from pydantic import BaseModel
class AuthResponse(BaseModel):
    authId: int
    tipoAuth: enum.Enum
    escritorioId: int
    advogadoId: int
    authDeOnde: enum.Enum
    horaAuth: datetime
    dataCadastro: datetime


class AuthRequest(BaseModel):
    authId: Optional[int]
    tipoAuth: enum.Enum
    escritorioId: Optional[int]
    advogadoId: Optional[int]
    horaAuth: datetime
    authDeOnde: enum.Enum


class PrimeiroAcessoEsqueceuSenha(BaseModel):
    info: str
    esqueceuSenha: bool