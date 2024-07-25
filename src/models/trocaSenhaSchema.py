from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TrocaSenhaSchema(BaseModel):
    acessoId: int
    escritorioId: Optional[int]
    advogadoId: Optional[int]
    codAcesso: int
    primAcesso: bool
    verificado: bool = False
    # tipoTroca: EsqueceuSenhaPAcesso
    dataUltAlt: Optional[datetime] = datetime.now()
    dataCadastro: Optional[datetime] = None
