#SQLAlchemy primeiro
#Request e Responses em baixo

from datetime import datetime
from typing import Optional

from src.utils.enums.authEnums import EsqueceuSenhaPAcesso

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum, Boolean

from src.database.database import Base


class TrocaSenha(Base):
    __tablename__ = "TrocaSenha"

    acessoId = Column(Integer, primary_key=True, autoincrement=True)
    escritorioId = Column(Integer, ForeignKey("Escritorio.escritorioId"), nullable=True)
    advogadoId = Column(Integer, ForeignKey("Advogado.advogadoId"), nullable=True)
    codAcesso = Column(Integer, primary_key=True)
    primAcesso = Column(Boolean, nullable=False, default=True)
    tipoTroca = Column(Enum(EsqueceuSenhaPAcesso, values_callable=lambda obj: [e.value for e in obj]))
    dataUltAlt = Column(DateTime, default=datetime.now(), nullable=False)
    dataCadastro = Column(DateTime, default=datetime.now(), nullable=False)

    def __str__(self):
        return f"TrocaSenha({self.toDict()})"

    def toDict(self):
        return {
            "acessoId": self.acessoId,
            "escritorioId": self.escritorioId,
            "advogadoId": self.advogadoId,
            "codAcesso": self.codAcesso,
            "primAcesso": self.primAcesso,
            "tipoTroca": self.tipoTroca,
            "dataUltAlt": self.dataUltAlt,
            "dataCadastro": self.dataCadastro,
        }


from pydantic import BaseModel
class TrocaSenhaSchema(BaseModel):
    acessoId: int
    escritorioId: Optional[int]
    advogadoId: Optional[int]
    codAcesso: int
    primAcesso: bool
    tipoTroca: EsqueceuSenhaPAcesso
    dataUltAlt: datetime
    dataCadastro: datetime