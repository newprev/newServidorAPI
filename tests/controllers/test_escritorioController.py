from fastapi.testclient import TestClient
from httpx import Response

from main import app
from src.models.escritoriosModel import EscritorioResponse

HEADERS = {"content-type": "application/json"}

client = TestClient(app)
escritorioId: int = 1


def test_deve_encontrar_pelo_menos_um_escritorio():
    response: Response = client.get("/escritorio/all")

    assert response.status_code == 200
    assert len(response.json()) > 0


def test_deve_encontrar_escritorio_pelo_Id():
    response: Response = client.get(f"/escritorio/{escritorioId}")

    assert response.status_code == 200
    assert EscritorioResponse(**response.json())

def test_deve_voltar_status_404_por_nao_encontrar_escritorio():
    response: Response = client.get(f"/escritorio/666")

    assert response.status_code == 404


def test_DEVE_inserir_novo_escritorio():
    novoEscritorio: dict = {
        "nomeFantasia": "Teste_Automatizado",
        "cnpj": "123456789",
        "telefone": "11123456789",
        "email": "teste.automatizado@gmail.com",
        "inscEstadual": "12345678",
        "endereco": "Rua Teste automatizado",
        "numero": 10,
        "cep": "03325458",
        "complemento": "",
        "cidade": "Sâo Paulo",
        "estado": "SP",
        "bairro": "Tatuapé"
    }
    response: Response = client.post(f"/escritorio/", json=novoEscritorio, headers=HEADERS)

    assert response.status_code == 201

def test_DEVE_excluir_escritorio_e_endereco():
    responseGet: Response = client.get(f"/escritorio/all")
    ultimoEscritorioId = responseGet.json()[-1]["escritorioId"]

    response: Response = client.delete(f"/escritorio/{ultimoEscritorioId}")

    assert response.status_code == 200

