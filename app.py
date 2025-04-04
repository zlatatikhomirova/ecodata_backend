from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def create_app():
    app: FastAPI = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['http://localhost:3000'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
