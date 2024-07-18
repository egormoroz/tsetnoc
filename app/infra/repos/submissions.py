import dataclasses

from sqlalchemy import func, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from app.common.errors import ErrorCode, MalformedError
from app.common.interfaces import ISubRepo

import app.core.models as core
import app.infra.models as infra


# for brevity
Sub = infra.Submission


class SQLSubRepo(ISubRepo):
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    async def add_checked(self, sub: core.Submission) -> int:
        data = dataclasses.asdict(sub)
        del data["id"]
        stmt = insert(Sub).values(data).returning(Sub.id)
        try:
            async with self.session() as sess, sess.begin():
                result = await sess.execute(stmt)
                sub.id = result.scalar_one()
                return sub.id
        except IntegrityError as e:
            e = str(e.orig)
            if "FOREIGN KEY" in e:
                raise MalformedError(ErrorCode.FOREIGN_KEY_ERROR)
            elif "UNIQUE" in e:
                raise MalformedError(ErrorCode.ALREADY_EXISTS)
            raise

    async def count_tries(self, user_id: int, prob_id: int, cont_id: int) -> int:
        query = select(func.count()).select_from(Sub).where(
            Sub.author_id == user_id,
            Sub.prob_id == prob_id,
            Sub.contest_id == cont_id,
        )
        async with self.session() as sess:
            result = await sess.execute(query)
            return result.scalar_one()

    async def get_ids_by(
        self, 
        uid: int, 
        pid: int|None=None, 
        cid: int|None=None,
    ) -> list[int]:
        clauses = [Sub.author_id == uid]
        if pid is not None:
            clauses.append(Sub.prob_id == pid)
        if cid is not None:
            clauses.append(Sub.contest_id == cid)
        query = select(Sub.id).where(*clauses)

        async with self.session() as sess:
            result = await sess.execute(query)
            return list(result.scalars().all())

    async def get_by(
        self, 
        uid: int, 
        pid: int|None=None, 
        cid: int|None=None,
    ) -> list[core.Submission]:
        Sub = infra.Submission
        clauses = [Sub.author_id == uid]
        if pid is not None:
            clauses.append(Sub.prob_id == pid)
        if cid is not None:
            clauses.append(Sub.contest_id == cid)
        query = select(Sub).where(*clauses)

        async with self.session() as sess:
            result = await sess.execute(query)
        return [
            core.Submission(
                id=sub.id,
                author_id=sub.author_id,
                prob_id=sub.prob_id,
                contest_id=sub.contest_id,
                answer=sub.answer,
                verdict=sub.verdict,
                n_try=sub.n_try
            ) for sub in result.scalars().all()
        ]
