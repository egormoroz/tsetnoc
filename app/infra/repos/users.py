from sqlalchemy import exists, select, insert, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from app.common.interfaces import IUserRepo

import app.core.models as core
import app.infra.models as infra


class SQLUserRepo(IUserRepo):
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    async def add(self, user: core.User) -> int:
        data = user.model_dump()
        del data["id"]
        async with self.session() as sess, sess.begin():
            stmt = insert(infra.User).values(data).returning(infra.User.id)
            result = await sess.execute(stmt)
            user.id = result.scalar_one()
            return user.id

    async def get(self, id: int) -> core.User | None:
        async with self.session() as sess:
            query = select(infra.User).where(infra.User.id == id)
            u = await sess.execute(query)
        u = u.scalar_one_or_none()
        if u is None:
            return None
        return core.User.model_validate(u, from_attributes=True)

    async def can_see_problem(self, uid: int, pid: int) -> bool:
        c_prob = infra.ContestProblem
        c_part = infra.ContestParticipant

        query = select(exists().where(
            and_(
                infra.Contest.id == c_prob.contest_id,
                c_prob.problem_id == pid,
                infra.Contest.id == c_part.contest_id,
                c_part.user_id == uid
            )
        ))

        async with self.session() as sess:
            result = await sess.execute(query)
            return result.scalar_one()

    async def get_ids_by_contest(self, cont_id: int) -> list[int]:
        cp = infra.ContestParticipant
        query = select(cp.user_id).where(cp.contest_id == cont_id)
        async with self.session() as sess:
            result = await sess.execute(query)
            return list(result.scalars().all())

    async def joined_contest(self, uid: int, cid: int) -> bool:
        cp = infra.ContestParticipant
        query = (
            select(cp)
            .where(cp.contest_id == cid, cp.user_id == uid)
            .limit(1) # ugly
        )
        async with self.session() as sess:
            result = await sess.execute(query)
            return result.scalar_one_or_none() is not None

    async def all(self) -> list[core.User]:
        async with self.session() as sess:
            result = await sess.execute(select(infra.User))
        return [
            core.User.model_validate(u, from_attributes=True)
            for u in result.scalars().all()
        ]
