import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.infra.models import Base
from app.core.models import (
    Problem, ReservedTags, User, Contest, Submission, Verdict
)
from app.infra.repos import (
    SQLProblemRepo, SQLUserRepo, SQLTagRepo, SQLContestRepo, SQLSubRepo
)


@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine("sqlite+aiosqlite:///test.db", echo=False)
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


@pytest.fixture(scope="function")
async def insert_tags(session):
    tags = ReservedTags.make()
    tag_repo = SQLTagRepo(session)
    await tag_repo.add_many(tags, keep_ids=True)
    return tags, tag_repo


@pytest.fixture(scope="function")
async def insert_problems(session, insert_tags):
    problems = [
        Problem(id=1, name="Problem 1", max_tries=3, tags={1, 2}, 
                     content="Content 1", answer="Answer 1"),
        Problem(id=2, name="Problem 2", max_tries=5, tags={2}, 
                     content="Content 2", answer="Answer 2"),
    ]
    repo = SQLProblemRepo(session)
    await repo.add_many(problems)
    return problems, repo


@pytest.fixture(scope="function")
async def insert_users(session):
    users = [
        User.new("User 1"), User.new("User 2")
    ]
    user_repo = SQLUserRepo(session)
    for u in users:
        await user_repo.add(u)
    return users, user_repo


@pytest.fixture(scope="function")
async def insert_contest(session):
    contest = Contest(id=0, name="contest 1")
    cont_repo = SQLContestRepo(session)
    await cont_repo.add(contest)
    return contest, cont_repo


@pytest.fixture(scope="function")
async def insert_subs(
    session,
    insert_users: tuple[list[User], SQLUserRepo],
    insert_problems: tuple[list[Problem], SQLProblemRepo], 
    insert_contest: tuple[Contest, SQLContestRepo],
):
    users, _ = insert_users
    problems, _ = insert_problems
    contest, _ = insert_contest

    subs = [
        Submission(
            id=0, 
            author_id=users[0].id, 
            prob_id=problems[0].id,
            contest_id=contest.id,

            answer="answer 1",
            n_try=1,
            verdict=Verdict.ACCEPTED,
        ),
        Submission(
            id=0, 
            author_id=users[0].id, 
            prob_id=problems[1].id,
            contest_id=contest.id,

            answer="wrong answer 1",
            n_try=1,
            verdict=Verdict.WRONG,
        ),
        Submission(
            id=0, 
            author_id=users[0].id, 
            prob_id=problems[1].id,
            contest_id=contest.id,

            answer="wrong answer 2",
            n_try=2,
            verdict=Verdict.WRONG,
        ),
        Submission(
            id=0, 
            author_id=users[1].id, 
            prob_id=problems[0].id,
            contest_id=contest.id,

            answer="wrong answer 1",
            n_try=1,
            verdict=Verdict.WRONG,
        ),
    ]
    sub_repo = SQLSubRepo(session)
    for sub in subs:
        await sub_repo.add_checked(sub)
    return subs, sub_repo

