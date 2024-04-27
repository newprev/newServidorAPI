import uvicorn
from fastapi import FastAPI

from controller.healthCheck import healthCheckRouter
app = FastAPI()

#Incluindo rotas
app.include_router(healthCheckRouter)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
