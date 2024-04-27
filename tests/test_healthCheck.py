from fastapi.testclient import TestClient
from httpx import Response

from main import app

client = TestClient(app)

def testando_healthCheck():
    response: Response = client.get("/healthCheck/ping")
    assert response.status_code == 200
    assert response.json()['statusService'] == "online"