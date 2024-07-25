from pydantic import BaseModel

from src.models.advogadosSchema import AdvogadoResponse
from src.models.enderecoSchema import EnderecoResponse
from src.models.escritorioSchema import EscritorioResponse


class AdvogadoEscritorio(BaseModel):
    advogado: AdvogadoResponse
    escritorio: EscritorioResponse
    endereco: EnderecoResponse
