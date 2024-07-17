import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import app.infra.models as infra
import app.core.models as core
from app.infra.repos.problems import SQLProblemRepo


@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine("sqlite+aiosqlite:///test.db", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(infra.Base.metadata.drop_all)
        await conn.run_sync(infra.Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture(scope="function")
async def session(engine):
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    yield async_session
    async with engine.begin() as conn:
        await conn.run_sync(infra.Base.metadata.drop_all)
        await conn.run_sync(infra.Base.metadata.create_all)


@pytest.fixture(scope="function")
async def insert_problems(session):
    async with session() as sess, sess.begin():
        tag1 = infra.Tag(id=1)
        tag2 = infra.Tag(id=2)
        sess.add_all([tag1, tag2])
        sess.add_all([infra.TagInfo(id=1, name="easy"), 
                      infra.TagInfo(id=2, name="hard")])

    problems = [
        core.Problem(id=1, name="Problem 1", max_tries=3, tags={1, 2}, 
                     content="Content 1", answer="Answer 1"),
        core.Problem(id=2, name="Problem 2", max_tries=5, tags={2}, 
                     content="Content 2", answer="Answer 2"),
    ]
    repo = SQLProblemRepo(session)
    await repo.add_many(problems)
    return problems, repo

