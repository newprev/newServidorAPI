from fastapi.testclient import TestClient
from httpx import Response
from models.escritoriosModel import EscritorioResponse

from main import app

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
