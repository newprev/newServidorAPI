#SQLAlchemy primeiro
#Request e Responses em baixo
from datetime import datetime
from pydantic import BaseModel

class HealthCheckResponse(BaseModel):
    statusService: str
    horaRequest: datetime
    horaResponse: datetime
