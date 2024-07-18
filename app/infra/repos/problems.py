from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlalchemy.orm import selectinload
from app.common.errors import MalformedError
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
                await sess.execute(insert(infra.problem_tag).values(prob_tag_data))

            for p, pid in zip(problems, prob_ids):
                p.id = pid
            return list(prob_ids)
        except IntegrityError as e:
            if "FOREIGN KEY" in str(e.orig):
                raise MalformedError()
            raise

    async def get_ids_by_contest(self, cont_id: int) -> list[int]:
        async with self.session() as sess:
            query = select(infra.contest_problem.c.problem_id).where(
                infra.contest_problem.c.contest_id==cont_id)
            result = await sess.execute(query)
            return list(result.scalars().all())

    async def get_by_contest(self, cont_id: int) -> list[core.Problem]:
        query = (
            select(infra.Problem)
            .options(selectinload(infra.Problem.tags))
            .join(infra.contest_problem)
            .join(infra.problem_tag)
            .where(infra.contest_problem.c.contest_id == cont_id)
            .group_by(infra.Problem.id)
        )
        async with self.session() as sess:
            result = await sess.execute(query)
            problems_with_tags = result.scalars().all()
        return [
            core.Problem(
                id=p.id,
                name=p.name,
                max_tries=p.max_tries,
                content=p.content,
                answer=p.answer,
                tags=set([t.id for t in p.tags])
            ) for p in problems_with_tags
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
        return core.Problem(
            id=p.id,
            name=p.name,
            max_tries=p.max_tries,
            content=p.content,
            answer=p.answer,
            tags=set(tag.id for tag in p.tags)
        )

