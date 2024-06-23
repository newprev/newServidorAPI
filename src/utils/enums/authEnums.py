from enum import Enum


class TipoAuth(Enum):
    escritorio = 'E'
    advogado = 'A'
    Super = 'S'


class AuthDeOnde(Enum):
    site = 'S'
    mobile = 'M'
    desktop = 'D'

class EsqueceuSenhaPAcesso(Enum):
    esqueceuSenha = 'ES'
    primeiroAcesso = 'PA'
