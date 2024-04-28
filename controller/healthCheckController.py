import datetime

from fastapi import APIRouter
from models.healthCheck import HealthCheckResponse

TAG_PREFIX = "/healthCheck"
healthCheckRouter = APIRouter(prefix=TAG_PREFIX, tags=[TAG_PREFIX])


@healthCheckRouter.get('/ping', response_model=HealthCheckResponse, status_code=200)
def healthCheack() -> HealthCheckResponse:
    """
    Retorna status do serviço do NewPrev
    """
    hc = HealthCheckResponse(
        horaRequest=datetime.datetime.now(),
        statusService="online",
        horaResponse=datetime.datetime.now()
    )

    return hc

