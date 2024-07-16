from typing import override
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from app.common.interfaces import IProblemRepo

import app.core.models as core
import app.infra.models as infra


class SQLProblemRepo(IProblemRepo):
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    @override
    async def add_many(self, problems: list[core.Problem]) -> list[int]:
        raise NotImplementedError

    @override
    async def get_ids_by_contest(self, cont_id: int) -> list[int]:
        raise NotImplementedError

    @override
    async def get_by_contest(self, cont_id: int) -> list[core.Problem]:
        raise NotImplementedError
