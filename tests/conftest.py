import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.infra.models import Base


@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine("sqlite+aiosqlite:///test.db", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture(scope="function")
async def session(engine):
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    yield async_session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# @pytest.fixture(scope="function")
# async def setup_test_data(session):
#     # Add any test data you need here
#     # For example:
#     from app.infra.models import Tag
#     tag1 = Tag(id=1, name="Math")
#     tag2 = Tag(id=2, name="Easy")
#     session.add_all([tag1, tag2])
#     await session.commit()
