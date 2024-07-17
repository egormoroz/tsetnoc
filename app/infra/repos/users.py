import dataclasses
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
        data = dataclasses.asdict(user)
        del data["id"]
        async with self.session() as sess, sess.begin():
            stmt = insert(infra.User).values(data).returning(infra.User.id)
            result = await sess.execute(stmt)
            return result.scalar_one()

    async def get(self, id: int) -> core.User | None:
        async with self.session() as sess:
            query = select(infra.User).filter(infra.User.id == id)
            u = await sess.execute(query)
        u = u.scalar_one_or_none()
        if u is None:
            return None
        return core.User(id=u.id, name=u.name, n_submissions=u.n_submissions,
                         probs_tried=u.probs_tried, probs_solved=u.probs_solved)

    async def can_see_problem(self, uid: int, pid: int) -> bool:
        c_prob = infra.contest_problem
        c_part = infra.contest_participant

        query = select(exists().where(
            and_(
                infra.Contest.id == c_prob.c.contest_id,
                c_prob.c.problem_id == pid,
                infra.Contest.id == c_part.c.contest_id,
                c_part.c.user_id == uid
            )
        ))

        async with self.session() as sess:
            result = await sess.execute(query)
            return result.scalar_one()

    async def get_by_contest(self, cont_id: int) -> list[int]:
        cp = infra.contest_participant
        query = select(infra.User.id).where(cp.c.contest_id == cont_id)
        async with self.session() as sess:
            result = await sess.execute(query)
            return [i for i in result.scalars().all()]

    async def joined_contest(self, uid: int, cid: int) -> bool:
        cp = infra.contest_participant
        query = select(exists()).where(cp.c.contest_id == cid, cp.c.user_id == uid)
        async with self.session() as sess:
            result = await sess.execute(query)
            return result.scalar_one()