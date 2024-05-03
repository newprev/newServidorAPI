from typing import List

from fastapi.testclient import TestClient
from httpx import Response
from models.advogadosModel import AdvogadoResponse

from main import app

client = TestClient(app)
enderecoId: int = 1


def test_deve_encontrar_algum_endereco():
    response: Response = client.get("/endereco/all")

    assert response.status_code == 200
    assert response.json() is List


def test_deve_encontrar_advogado_pelo_Id():
    response: Response = client.get(f"/endereco/{enderecoId}")

    assert response.status_code == 200
    assert AdvogadoResponse(**response.json())

def test_deve_voltar_status_404_por_nao_encontrar_advogado():
    response: Response = client.get(f"/advogado/666")

    assert response.status_code == 404
