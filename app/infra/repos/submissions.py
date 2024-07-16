from typing import override
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from app.common.interfaces import ISubRepo

import app.core.models as core
import app.infra.models as infra


class SQLSubRepo(ISubRepo):
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    @override
    async def add_checked(self, sub: core.Submission) -> int:
        raise NotImplementedError

    @override
    async def count_tries(self, user_id: int, prob_id: int, cont_id: int) -> int:
        raise NotImplementedError

    @override
    async def get(self, id: int) -> core.Submission|None:
        raise NotImplementedError

    @override
    async def get_ids_by(self, uid: int, pid: int|None, cid: int|None) -> list[int]:
        raise NotImplementedError

    @override
    async def get_by(
            self, 
            uid: int, 
            pid: int|None, 
            cid: int|None) -> list[core.Submission]:
        raise NotImplementedError
