import pytest

from app.infra.repos import (
    SQLProblemRepo, SQLContestRepo, SQLUserRepo, SQLTagRepo
)
import app.core.models as core


def problems_match(got_probs, expected_probs):
    assert len(got_probs) == len(expected_probs)
    for got, expected in zip(got_probs, expected_probs):
        assert got.name == expected.name
        assert got.max_tries == expected.max_tries
        assert got.content == expected.content
        assert got.answer == expected.answer
        assert got.tags == expected.tags


@pytest.mark.asyncio
async def test_insert_get_tags(session):
    tag_repo = SQLTagRepo(session)
    tags = core.ReservedTags.make()

    ids = await tag_repo.add_many(tags, keep_ids=True)
    assert ids == [t.id for t in tags]

    got_tags = await tag_repo.get_many(ids)
    assert got_tags == tags


@pytest.mark.asyncio
async def test_insert_get_problems(session, insert_tags):
    prob_repo = SQLProblemRepo(session)

    problems = [
        core.Problem(id=0, name="Problem 1", max_tries=3, tags={1, 2}, 
                     content="Content 1", answer="Answer 1"),
        core.Problem(id=0, name="Problem 2", max_tries=5, tags={2}, 
                     content="Content 2", answer="Answer 2"),
    ]

    inserted_ids = await prob_repo.add_many(problems)
    assert inserted_ids == [p.id for p in problems]

    db_problems = [await prob_repo.get(i) for i in inserted_ids]
    problems_match(db_problems, problems)


@pytest.mark.asyncio
async def test_insert_get_problems_contest(session, insert_problems):
    problems: list[core.Problem] = insert_problems[0]
    prob_repo: SQLProblemRepo = insert_problems[1]
    cont_repo = SQLContestRepo(session)

    prob_ids = [p.id for p in problems]

    cid = await cont_repo.add(core.Contest(id=0, name="contest 1"))
    await cont_repo.add_problems(cid, prob_ids)

    got_ids = await prob_repo.get_ids_by_contest(cid)
    assert set(got_ids) == set(prob_ids)

    got = await prob_repo.get_by_contest(cid)
    got.sort(key=lambda p: p.id)
    problems_match(got, problems)


@pytest.mark.asyncio
async def test_add_get_users(session):
    users = [
        core.User.new("User 1"), core.User.new("User 2")
    ]
    user_repo = SQLUserRepo(session)
    for u in users:
        await user_repo.add(u)

    # for expected in users:
    #     got = await user_repo.get(expected.id)
    #     assert got.name == expected.name


@pytest.mark.asyncio
async def test_join_contest_get_by_contest(
    session,
    insert_users: tuple[list[core.User], SQLUserRepo]
):
    users, user_repo = insert_users



@pytest.mark.asyncio
async def test_create_contest(session):
    pass
