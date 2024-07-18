import pytest
from collections import Counter

from app.infra.repos import (
    SQLProblemRepo, SQLContestRepo, SQLUserRepo, SQLTagRepo, SQLSubRepo
)
from app.core.models import Problem, User, ReservedTags, Contest, Submission, Verdict


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
    tags = ReservedTags.make()

    ids = await tag_repo.add_many(tags, keep_ids=True)
    assert ids == [t.id for t in tags]

    got_tags = await tag_repo.get_many(ids)
    assert got_tags == tags


@pytest.mark.asyncio
async def test_insert_get_problems(session, insert_tags):
    prob_repo = SQLProblemRepo(session)

    problems = [
        Problem(id=0, name="Problem 1", max_tries=3, tags={1, 2}, 
                     content="Content 1", answer="Answer 1"),
        Problem(id=0, name="Problem 2", max_tries=5, tags={2}, 
                     content="Content 2", answer="Answer 2"),
    ]

    inserted_ids = await prob_repo.add_many(problems)
    assert inserted_ids == [p.id for p in problems]

    db_problems = [await prob_repo.get(i) for i in inserted_ids]
    problems_match(db_problems, problems)


@pytest.mark.asyncio
async def test_insert_get_problems_contest(session, insert_problems):
    problems: list[Problem] = insert_problems[0]
    prob_repo: SQLProblemRepo = insert_problems[1]
    cont_repo = SQLContestRepo(session)

    prob_ids = [p.id for p in problems]

    cid = await cont_repo.add(Contest(id=0, name="contest 1"))
    await cont_repo.add_problems(cid, prob_ids)

    got_ids = await prob_repo.get_ids_by_contest(cid)
    assert got_ids == prob_ids

    got = await prob_repo.get_by_contest(cid)
    problems_match(got, problems)


@pytest.mark.asyncio
async def test_add_get_users(session):
    users = [User.new("User 1"), User.new("User 2")]
    user_repo = SQLUserRepo(session)
    for u in users:
        await user_repo.add(u)

    for expected in users:
        got = await user_repo.get(expected.id)
        assert got.name == expected.name


@pytest.mark.asyncio
async def test_user_join_contest_get_by_contest(
    session,
    insert_users: tuple[list[User], SQLUserRepo],
    insert_contest: tuple[Contest, SQLContestRepo],
):
    users, user_repo = insert_users
    contest, cont_repo = insert_contest

    uids = [u.id for u in users[:-1]]
    await cont_repo.add_participants(contest.id, uids)

    uids_got = await user_repo.get_ids_by_contest(contest.id)
    assert uids == uids_got


    for uid in uids:
        assert await user_repo.joined_contest(uid, contest.id)
    assert not await user_repo.joined_contest(users[-1].id, contest.id)


@pytest.mark.asyncio
async def test_user_problem_visibility(
    session,
    insert_users: tuple[list[User], SQLUserRepo],
    insert_problems: tuple[list[Problem], SQLProblemRepo], 
    insert_contest: tuple[Contest, SQLContestRepo],
):
    users, user_repo = insert_users
    problems, _ = insert_problems
    contest, cont_repo = insert_contest

    uids = [u.id for u in users]
    pids = [p.id for p in problems]
    await cont_repo.add_participants(contest.id, uids[:-1])
    await cont_repo.add_problems(contest.id, pids[:-1])

    assert await user_repo.can_see_problem(uids[0], pids[0])
    assert not await user_repo.can_see_problem(uids[0], pids[-1])

    assert not await user_repo.can_see_problem(uids[-1], pids[0])
    assert not await user_repo.can_see_problem(uids[-1], pids[-1])
    

@pytest.mark.asyncio
async def test_add_sub(
    session,
    insert_users: tuple[list[User], SQLUserRepo],
    insert_problems: tuple[list[Problem], SQLProblemRepo], 
    insert_contest: tuple[Contest, SQLContestRepo],
):
    users, _ = insert_users
    problems, _ = insert_problems
    contest, _ = insert_contest

    sub_repo = SQLSubRepo(session)
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
            author_id=users[1].id, 
            prob_id=problems[0].id,
            contest_id=contest.id,

            answer="wrong answer 1",
            n_try=1,
            verdict=Verdict.WRONG,
        ),
    ]

    sub_ids = [await sub_repo.add_checked(sub) for sub in subs]
    assert sub_ids == [sub.id for sub in subs]


@pytest.mark.asyncio
async def test_sub_bulk_get(
    session,
    insert_subs: tuple[list[Submission], SQLSubRepo],
):
    subs, sub_repo = insert_subs

    uid = subs[0].author_id
    ids = await sub_repo.get_ids_by(uid)
    assert ids == [sub.id for sub in subs if sub.author_id == uid]

    uid = subs[0].author_id
    pid = subs[0].prob_id
    ids = await sub_repo.get_ids_by(uid, pid)
    assert ids == [sub.id for sub in subs if sub.author_id == uid and sub.prob_id == pid]


@pytest.mark.asyncio
async def test_sub_count_tries(
    session,
    insert_subs: tuple[list[Submission], SQLSubRepo],
):
    subs, sub_repo = insert_subs
    tries = Counter()
    for sub in subs:
        key = (sub.author_id, sub.prob_id, sub.contest_id)
        tries[key] += 1

    for sub in subs:
        key = (sub.author_id, sub.prob_id, sub.contest_id)
        tries_got = await sub_repo.count_tries(*key)
        assert tries_got == tries[key]
