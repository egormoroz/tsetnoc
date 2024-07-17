from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlalchemy.orm import joinedload
from app.common.interfaces import IProblemRepo

import app.core.models as core
import app.infra.models as infra


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

        async with self.session() as sess, sess.begin():
            stmt = insert(infra.Problem).values(prob_data).returning(infra.Problem.id)
            result = await sess.execute(stmt)
            prob_ids = result.scalars().all()

            prob_tag_data = [
                {"problem_id": pid, "tag_id": tag_id}
                for p, pid in zip(problems, prob_ids)
                for tag_id in p.tags
            ]
            await sess.execute(insert(infra.problem_tag).values(prob_tag_data))

        return [i for i in prob_ids]

    async def get_ids_by_contest(self, cont_id: int) -> list[int]:
        async with self.session() as sess:
            query = select(infra.contest_problem.c.problem_id).where(
                infra.contest_problem.c.contest_id==cont_id)
            result = await sess.execute(query)
            return [i for i in result.scalars().all()]

    async def get_by_contest(self, cont_id: int) -> list[core.Problem]:
        query = (
            select(infra.Problem)
            .join(infra.contest_problem)
            .where(infra.contest_problem.c.contest_id == cont_id)
            .options(joinedload(infra.Problem.tags))
        )
        async with self.session() as sess:
            result = await sess.execute(query)
            problems = result.scalars().all()
        return [
            core.Problem(
                id=p.id,
                name=p.name,
                max_tries=p.max_tries,
                content=p.content,
                answer=p.answer,
                tags=set(p.tags)
            ) for p in problems
        ]

    async def get(self, id: int) -> core.Problem | None:
        query = select(infra.Problem).options(joinedload(infra.Problem.tags))
        async with self.session() as sess:
            result = await sess.execute(query)
            p = result.scalar_one_or_none()
        if p is None:
            return None
        return core.Problem(
            id=p.id,
            name=p.name,
            max_tries=p.max_tries,
            content=p.content,
            answer=p.answer,
            tags=set(p.tags)
        )

