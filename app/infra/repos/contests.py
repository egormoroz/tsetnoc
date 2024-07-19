from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from app.common.errors import ErrorCode, MalformedError
from app.common.interfaces import IContestRepo

import app.core.models as core
import app.infra.models as infra


# for brevity
Cont = infra.Contest


class SQLContestRepo(IContestRepo):
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    async def add(self, contest: core.Contest) -> int:
        values = contest.model_dump()
        del values["id"]
        async with self.session() as sess, sess.begin():
            stmt = insert(Cont).values(values).returning(Cont.id)
            result = await sess.execute(stmt)
            contest.id = result.scalar_one()
            return contest.id

    async def add_participants(self, cid: int, uids: list[int]):
        stmt = insert(infra.contest_participant).values(
            [{"contest_id": cid, "user_id": uid} for uid in uids]
        )
        try:
            async with self.session() as sess, sess.begin():
                await sess.execute(stmt)
        except IntegrityError as e:
            e = str(e.orig)
            if "FOREIGN KEY" in e:
                raise MalformedError(ErrorCode.FOREIGN_KEY_ERROR)
            elif "UNIQUE" in e:
                raise MalformedError(ErrorCode.ALREADY_EXISTS)
            raise


    async def add_problems(self, cid: int, pids: list[int]):
        stmt = insert(infra.contest_problem).values(
            [{"contest_id": cid, "problem_id": pid} for pid in pids]
        )
        try:
            async with self.session() as sess, sess.begin():
                await sess.execute(stmt)
        except IntegrityError as e:
            e = str(e.orig)
            if "FOREIGN KEY" in e:
                raise MalformedError(ErrorCode.FOREIGN_KEY_ERROR)
            elif "UNIQUE" in e:
                raise MalformedError(ErrorCode.ALREADY_EXISTS)
            raise

    async def all(self) -> list[core.Contest]:
        async with self.session() as sess:
            result = await sess.execute(select(Cont))
        return [
            core.Contest.model_validate(c, from_attributes=True)
            for c in result.scalars().all()
        ]


