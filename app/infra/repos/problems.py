from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlalchemy.orm import selectinload
from app.common.errors import MalformedError, ErrorCode
from app.common.interfaces import IProblemRepo

import app.core.models as core
import app.infra.models as infra


# evil magic
class _Wrapper:
    def __init__(self, p: infra.Problem):
        self._p = p

    def __getattr__(self, name):
        if name == "tags":
            return set(t.id for t in self._p.tags)
        return getattr(self._p, name)


class SQLProblemRepo(IProblemRepo):
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    async def add_many(self, problems: list[core.Problem]) -> list[int]:
        prob_data = [{
            "name": p.name,
            "max_tries": p.max_tries,
            "content": p.content,
            "answer": p.answer
        } for p in problems]

        try:
            async with self.session() as sess, sess.begin():
                stmt = insert(infra.Problem).values(prob_data).returning(infra.Problem.id)
                result = await sess.execute(stmt)
                prob_ids = result.scalars().all()

                prob_tag_data = [
                    {"problem_id": pid, "tag_id": tag_id}
                    for p, pid in zip(problems, prob_ids)
                    for tag_id in p.tags
                ]
                if prob_tag_data:
                    await sess.execute(insert(infra.problem_tag).values(prob_tag_data))

            for p, pid in zip(problems, prob_ids):
                p.id = pid
            return list(prob_ids)
        except IntegrityError as e:
            e = str(e.orig)
            if "FOREIGN KEY" in e:
                raise MalformedError(ErrorCode.FOREIGN_KEY_ERROR)
            elif "UNIQUE" in e:
                raise MalformedError(ErrorCode.ALREADY_EXISTS)
            raise

    async def get_ids_by_contest(self, cont_id: int) -> list[int]:
        async with self.session() as sess:
            query = select(infra.contest_problem.c.problem_id).where(
                infra.contest_problem.c.contest_id==cont_id)
            result = await sess.execute(query)
            return list(result.scalars().all())

    async def get_by_contest(self, cont_id: int) -> list[core.Problem]:
        cp = infra.contest_problem
        query = (
            select(infra.Problem)
            .options(selectinload(infra.Problem.tags))
            .where(cp.c.contest_id == cont_id, 
                   cp.c.problem_id == infra.Problem.id)
        )
        async with self.session() as sess:
            result = await sess.execute(query)
            problems_with_tags = result.scalars().all()
        return [
            core.Problem.model_validate(_Wrapper(p), from_attributes=True)
            for p in problems_with_tags
        ]

    async def get(self, id: int) -> core.Problem | None:
        query = (
            select(infra.Problem)
            .options(selectinload(infra.Problem.tags))
            .where(infra.Problem.id == id)
        )
        async with self.session() as sess:
            result = await sess.execute(query)
            p = result.scalar_one_or_none()
        return core.Problem.model_validate(_Wrapper(p), from_attributes=True)
