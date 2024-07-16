from typing import override
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from app.common.interfaces import IUserRepo

import app.core.models as core
import app.infra.models as infra


class SQLUserRepo(IUserRepo):
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    @override
    async def add(self, user: core.User) -> int:
        async with self.session() as sess:
            u = infra.User(**user.__dict__)
            sess.add(u)
            await sess.commit()
            await sess.refresh(u)
            return u.id

    @override
    async def get(self, id: int) -> core.User | None:
        async with self.session() as sess:
            query = select(infra.User).filter(infra.User.id == id)
            u = await sess.execute(query)
        u = u.scalar_one_or_none()
        if u is None:
            return None
        return core.User(id=u.id, name=u.name, n_submissions=u.n_submissions,
                         probs_tried=u.probs_tried, probs_solved=u.probs_solved)

    @override
    async def can_see_problem(self, uid: int, pid: int) -> bool:
        # TODO: check if user has joined any contest which has problem with index pid
        raise NotImplementedError
