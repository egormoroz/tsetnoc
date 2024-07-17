import pytest

from app.infra.repos import SQLProblemRepo, SQLContestRepo
import app.core.models as core
import app.infra.models as infra


def problems_match(got_probs, expected_probs):
    assert len(got_probs) == len(expected_probs)
    for got, expected in zip(got_probs, expected_probs):
        assert got.name == expected.name
        assert got.max_tries == expected.max_tries
        assert got.content == expected.content
        assert got.answer == expected.answer
        assert got.tags == expected.tags


@pytest.mark.asyncio
async def test_insert_problems(session):
    async with session() as sess, sess.begin():
        tag1 = infra.Tag(id=1)
        tag2 = infra.Tag(id=2)
        sess.add_all([tag1, tag2])

    prob_repo = SQLProblemRepo(session)

    problems = [
        core.Problem(id=0, name="Problem 1", max_tries=3, tags={1, 2}, content="Content 1", answer="Answer 1"),
        core.Problem(id=0, name="Problem 2", max_tries=5, tags={2}, content="Content 2", answer="Answer 2"),
    ]

    inserted_ids = await prob_repo.add_many(problems)
    assert inserted_ids == [1, 2]

    db_problems = [await prob_repo.get(i) for i in inserted_ids]
    problems_match(db_problems, problems)


@pytest.mark.asyncio
async def test_insert_problems_contest(session, insert_problems):
    problems: list[core.Problem] = insert_problems[0]
    prob_repo: SQLProblemRepo = insert_problems[1]
    cont_repo = SQLContestRepo(session)

    prob_ids = [p.id for p in problems]

    cid = await cont_repo.add(core.Contest(id=0, name="contest 1"))
    await cont_repo.add_problems(cid, prob_ids)

    got = await prob_repo.get_by_contest(cid)
    got.sort(key=lambda p: p.id)
    problems_match(got, problems)

