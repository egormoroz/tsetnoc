import dataclasses
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from app.common.interfaces import ITagRepo

import app.core.models as core
import app.infra.models as infra


class SQLTagRepo(ITagRepo):
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    async def add_many(self, tags: list[core.Tag], keep_ids=False) -> list[int]:
        data = [dataclasses.asdict(t) for t in tags]
        stmt = insert(infra.Tag).returning(infra.Tag.id)
        if keep_ids:
            stmt = stmt.values([{ "id": t.id } for t in tags])

        async with self.session() as sess, sess.begin():
            ids = (await sess.execute(stmt)).scalars().all()
            for d, i in zip(data, ids):
                d["id"] = i
            await sess.execute(insert(infra.TagInfo).values(data))

        if not keep_ids:
            for t, i in zip(tags, ids):
                t.id = i
        return list(ids)


    async def get_many(self, ids: list[int]) -> list[core.Tag]:
        stmt = select(infra.TagInfo).where(infra.TagInfo.id.in_(ids))
        async with self.session() as sess:
            result = await sess.execute(stmt)
        tags = result.scalars().all()
        return [
            core.Tag(id=t.id, name=t.name, description=t.description)
            for t in tags
        ]
