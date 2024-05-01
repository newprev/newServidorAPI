from fastapi.testclient import TestClient
from httpx import Response

from main import app

client = TestClient(app)


def test_healthCheck_deve_voltar_200():
    response: Response = client.get("/healthCheck/ping")
    assert response.status_code == 200
    assert response.json()['statusService'] == "online"