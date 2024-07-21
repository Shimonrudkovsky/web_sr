from typing import Optional, TypeVar

from psycopg import AsyncConnection
from psycopg.rows import dict_row
from pydantic import BaseModel


class DBConfig(BaseModel):
    host: str
    database: str
    user: str
    password: str


PostgresStorage = TypeVar("PostgresStorage", bound="AsyncPGStorage")


class AsyncPGStorage:
    conn: AsyncConnection

    def __init__(self, connection: AsyncConnection) -> None:
        self.conn = connection

    @classmethod
    async def init(cls, config: DBConfig) -> PostgresStorage:
        conn = await AsyncConnection.connect(
            host=config.host,
            dbname=config.database,
            user=config.user,
            password=config.password,
            row_factory=dict_row,
            autocommit=True,
        )

        return AsyncPGStorage(connection=conn)

    async def execute(self, query: str, params: Optional[tuple] = None):
        async with self.conn.cursor() as cur:
            await cur.execute(query=query, params=params)

    async def fetch(self, query: str, params: Optional[tuple] = None) -> dict:
        async with self.conn.cursor() as cur:
            await cur.execute(query=query, params=params)
            result = await cur.fetchall()

            return result
