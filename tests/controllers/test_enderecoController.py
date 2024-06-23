from typing import List

from fastapi.testclient import TestClient
from httpx import Response
from src.models.enderecoModel import EnderecoResponse

from main import app

client = TestClient(app)

corretoEnderecoId: int = 1
erradoEnderecoId: int = 1000
corretoEscritorioId: int = 1
erradoEscritorioId: int = 1000
corretoAdvogadoId: int = 1
erradoAdvogadoId: int = 1000


def test_DEVE_encontrar_algum_endereco():
    response: Response = client.get("/endereco/all")

    assert response.status_code == 200
    assert isinstance(response.json(), List)


def test_DEVE_encontrar_endereco_pelo_enderecoId():
    response: Response = client.get(f"/endereco/{corretoEnderecoId}")

    assert response.status_code == 200
    endCheck: EnderecoResponse = EnderecoResponse(**response.json())

    assert endCheck


def test_NAO_deve_encontrar_endereco_pelo_enderecoId_errado():
    response: Response = client.get(f"/endereco/{erradoEnderecoId}")

    assert response.status_code == 404
    assert response.json() == {'detail': 'Nenhum endereço encontrado'}


def test_DEVE_encontrar_endereco_dado_escritorioId_correto():
    response: Response = client.get(f"/endereco/escritorio/{corretoEscritorioId}")

    assert response.status_code == 200
    assert isinstance(response.json(), List)
    assert response.json()[0]['enderecoId'] is not None


def test_NAO_deve_encontrar_endereco_dado_escritorioId_errado():
    response: Response = client.get(f"/endereco/escritorio/{erradoEscritorioId}")

    assert response.status_code == 404
    assert response.json() == {'detail': 'Nenhum endereço encontrado'}


def test_DEVE_encontrar_endereco_dado_advogadoId_correto():
    response: Response = client.get(f"/endereco/advogado/{corretoAdvogadoId}")

    assert response.status_code == 200
    assert isinstance(response.json(), List)
    assert response.json()[0]['advogadoId'] is not None


def test_NAO_deve_encontrar_endereco_dado_advogadoId_errado():
    response: Response = client.get(f"/endereco/advogado/{erradoEscritorioId}")

    assert response.status_code == 404
    assert response.json() == {'detail': 'Nenhum endereço encontrado'}