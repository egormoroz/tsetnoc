import pytest

from app.common.interfaces import ISubRepo, IUserRepo, IProblemRepo
from app.core.models import Submission, User, Problem, PendingSub, Verdict
from app.core.process import SubProcessor


# TODO: create fake repos to test core


@pytest.mark.asyncio
async def test_sub_processor(
    session,
    insert_users: tuple[list[User], IUserRepo],
    insert_problems: tuple[list[Problem], IProblemRepo], 
    insert_subs: tuple[list[Submission], ISubRepo],
):
    _, user_repo = insert_users
    problems, prob_repo = insert_problems
    _, sub_repo = insert_subs

    # ASSUME: uid 1 have already sent 2 WA subs to prob 1 (in conftest)
    
    processor = SubProcessor(user_repo, prob_repo, sub_repo)
    pending = PendingSub(author_id=1, prob_id=1, contest_id=1, 
                             answer=problems[0].answer)
    sub = await processor.process(pending)
    assert sub.verdict == Verdict.ACCEPTED

    sub = await processor.process(pending)
    print(sub.n_try)
    assert sub.verdict == Verdict.TRY_LIMIT_EXCEEDED

