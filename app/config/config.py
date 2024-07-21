from typing import Optional, TypeVar, Union

from fastapi import APIRouter, FastAPI
from fsrs import FSRS
from pydantic import BaseModel
from starlette.types import Lifespan as StarletteLifespan

AppType = TypeVar("AppType", bound="FastAPI")


Lifespan = Optional[StarletteLifespan[AppType]]


class ConfigError(Exception):
    def __init__(self, message):
        self.message = "Config error: " + message
        super().__init__(self.message)


class DBConfig(BaseModel):
    host: str
    database: str
    user: str
    password: str


class Config:
    port: int
    routers: list[APIRouter]
    fsrs: FSRS
    lifespan: Lifespan
    db: DBConfig

    def __init__(
        self,
        port: int,
        routers: Union[list[APIRouter], None] = None,
        lifespan: Lifespan = None,
        db_cofig: Union[DBConfig, None] = None,
    ) -> None:
        self.port = port
        if not routers or routers == []:
            raise ConfigError("no routers found")
        self.routers = routers if routers else []
        if not db_cofig:
            raise ConfigError("no db config is found")
        self.fsrs = FSRS()
        self.lifespan = lifespan
        self.db = db_cofig
