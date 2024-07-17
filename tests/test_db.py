import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.future import select

from app.core.models import Problem
from app.infra.repos import SQLProblemRepo


# @pytest.mark.asyncio
# async def test_insert_problems(session):

#     prob_repo = SQLProblemRepo(session)

#     problems = [
#         Problem(id=0, name="Problem 1", max_tries=3, tags={1, 2}, content="Content 1", answer="Answer 1"),
#         Problem(id=0, name="Problem 2", max_tries=5, tags={2}, content="Content 2", answer="Answer 2"),
#     ]

#     inserted_ids = await prob_repo.add_many(problems)

#     assert len(inserted_ids) == 2
#     assert set(inserted_ids) == {1, 2}

#     # Check if problems were inserted correctly
#     result = await session.execute(select(Problem))
#     db_problems = result.scalars().all()
#     assert len(db_problems) == 2

#     for prob in db_problems:
#         assert prob.id in [1, 2]
#         assert prob.name in ["Problem 1", "Problem 2"]
#         assert prob.max_tries in [3, 5]
#         assert prob.content in ["Content 1", "Content 2"]
#         assert prob.answer in ["Answer 1", "Answer 2"]

    # Check if problem-tag associations were created correctly
    # for prob in db_problems:
    #     if prob.id == 1:
    #         assert len(prob.tags) == 2
    #         assert set(tag.id for tag in prob.tags) == {1, 2}
    #     elif prob.id == 2:
    #         assert len(prob.tags) == 1
    #         assert set(tag.id for tag in prob.tags) == {2}

@pytest.mark.asyncio
async def test_add_user(session):
    async with session() as sess:
        pass
