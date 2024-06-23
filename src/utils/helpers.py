from typing import List
from sqlalchemy_utils import Choice

frequenciaPlano = [
    ('ME', 'Mensal'),
    ('AN', 'Anual'),
    ('VI', 'Vitalicio'),
]


def buscaAdvNaLista(listaAdvogados: List, advogadoId: int):
    for adv in listaAdvogados:
        if adv.advogadoId == advogadoId:
            return adv

    return None


def listaFrequenciaPlanos():
    return frequenciaPlano

def getEstados():
    return [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins')
    ]


def getEstadosDict() -> dict:
    return {
        'SP': 'São Paulo',
        'AC': 'Acre',
        'AL': 'Alagoas',
        'AP': 'Amapá',
        'AM': 'Amazonas',
        'BA': 'Bahia',
        'CE': 'Ceará',
        'DF': 'Distrito Federal',
        'ES': 'Espírito Santo',
        'GO': 'Goiás',
        'MA': 'Maranhão',
        'MT': 'Mato Grosso',
        'MS': 'Mato Grosso do Sul',
        'MG': 'Minas Gerais',
        'PA': 'Pará',
        'PB': 'Paraíba',
        'PR': 'Paraná',
        'PE': 'Pernambuco',
        'PI': 'Piauí',
        'RJ': 'Rio de Janeiro',
        'RN': 'Rio Grande do Norte',
        'RO': 'Rondônia',
        'RR': 'Roraima',
        'SC': 'Santa Catarina',
        'SE': 'Sergipe',
        'TO': 'Tocantins'
    }


def decideEstado(siglaEstado: str) -> Choice:
    dictEstados: dict = getEstadosDict()[siglaEstado]
    return Choice(code=siglaEstado, value=dictEstados)


def getTipoAuth() -> List:
    return [
        ('E', 'Escritorio'),
        ('A', 'Advogado'),
        ('S', 'Super')
    ]


def getAuthDeOnde() -> List:
    return [
        ('S', 'Site'),
        ('M', 'Mobile'),
        ('D', 'Desktop')
    ]


def campoAlterado(campoOriginal, campoAlterado) -> bool:
    if campoAlterado is None or campoAlterado == '':
        return False
    return campoOriginal != campoAlterado
