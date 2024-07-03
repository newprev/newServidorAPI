from typing import Optional, Any

from pydantic import BaseModel, ConfigDict


class NewPrevErro(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    erro: Exception
    detalhes: str
    funcao: str
    observacao: Optional[str] = None
