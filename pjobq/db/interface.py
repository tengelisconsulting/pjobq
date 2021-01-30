from abc import ABC, abstractmethod

import asyncpg  # type: ignore

from ..apptypes import PgNotifyListener


class DB(ABC):
    "database interface, specific to Postgres"

    @abstractmethod
    async def init(self) -> None:
        "init the database connection.  should be idenpotent"
        pass

    @abstractmethod
    async def add_pg_notify_listener(self, channel: str, cb: PgNotifyListener) -> None:
        "add a listener for pg_notify events"
        return

    @abstractmethod
    async def fetch(self, sql: str, bindargs: list[str] = []) -> list[asyncpg.Record]:
        "fetch the results of an arbitrary aql query"
        pass