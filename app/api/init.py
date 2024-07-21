
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.config import Config


class FastAPI_(FastAPI):
    config: Config

    def __init__(self, config: Config, *args, **kwargs) -> None:
        super().__init__(lifespan=config.lifespan, *args, **kwargs)
        self.config: Config = config


class ServerGenerator:
    config: Config

    def __init__(self, config: Config) -> None:
        self.config = config

    def initWebServer(self) -> FastAPI:
        app = FastAPI_(config=self.config)

        # TODO: remove *
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Allows all origins
            allow_credentials=True,
            allow_methods=["*"],  # Allows all methods
            allow_headers=["*"],  # Allows all headers
        )

        for router in self.config.routers:
            app.include_router(router=router)

        app.state

        return app
