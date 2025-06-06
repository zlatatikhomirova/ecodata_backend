from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import router
from settings import settings


def create_app():
    print(settings)
    app: FastAPI = FastAPI()
    app.include_router(router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['http://localhost:3000'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
