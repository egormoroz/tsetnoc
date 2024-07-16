from typing import override
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from app.common.interfaces import IContestRepo

import app.core.models as core
import app.infra.models as infra


class SQLContestRepo(IContestRepo):
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    @override
    async def add(self, contest: core.Contest) -> int:
        raise NotImplementedError

    @override
    async def has(self, id: int) -> bool:
        raise NotImplementedError

    @override
    async def add_participants(self, cid: int, uids: list[int]):
        raise NotImplementedError

    @override
    async def add_problems(self, cid: int, pids: list[int]):
        raise NotImplementedError

    @override
    async def get_participants(self, cid: int) -> list[int]:
        raise NotImplementedError

    @override
    async def has_participant(self, cont_id: int, user_id: int) -> bool:
        raise NotImplementedError
