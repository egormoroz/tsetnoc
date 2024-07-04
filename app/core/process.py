from typing import Set

from app.infra.interfaces import IProblemRepo, ISubRepo, IContestRepo, IUserRepo
from .models import Problem, Submission, Verdict, Answer, ReservedTags


# hypothetically, can be an interface (but why?)
class SubProcessor:
    def __init__(
        self, 
        users: IUserRepo,
        problems: IProblemRepo, 
        submissions: ISubRepo, 
        contests: IContestRepo
    ):
        self._users = users
        self._probs = problems
        self._subs = submissions
        self._conts = contests

    def process(self, sub: Submission):
        # sanity check
        assert sub.verdict == Verdict.PENDING
        assert sub.id is None

        prob = self._get_problem(sub) # also checks if sub is valid
        if prob is None:
            sub.verdict = Verdict.SUB_MALFORMED
            return

        sub.n_try = 1 + self._subs.count_tries(
                sub.author_id, sub.prob_id, sub.contest_id)

        if ReservedTags.MAX_TRIES_UNLIMITED not in prob.tags \
                and sub.n_try > prob.max_tries:
            sub.verdict = Verdict.TRY_LIMIT_EXCEEDED
            return 

        sub.verdict = _compare_answers(sub.answer, prob.answer, prob.tags)
        sub.id = self._subs.add(sub)

    def _get_problem(self, sub: Submission) -> Problem | None:
        if not is_submission_valid(sub, self._users, self._probs, self._conts):
            return None
        # TODO: No need to retrieve the whole problem: 
        # only tags and answer are necessary
        return self._probs.get(sub.prob_id)


def is_submission_valid(
    sub: Submission, 
    ur: IUserRepo, 
    pr: IProblemRepo,
    cr: IContestRepo
) -> bool:
    cid = sub.contest_id
    if cid is not None:
        return cr.has_problem(cid, sub.prob_id) \
                and cr.has_participant(cid, sub.author_id)
    return ur.has(sub.author_id) and pr.has(sub.prob_id)


def _compare_answers(a: Answer, b: Answer, tags: Set[int]) -> Verdict:
    a_cont, b_cont = a.content, b.content

    if ReservedTags.ANS_DONT_TRIM not in tags:
        a_cont, b_cont = a_cont.strip(), b_cont.strip()
    if ReservedTags.ANS_CASE_INSENSETIVE in tags:
        a_cont, b_cont = a_cont.lower(), b_cont.lower()

    return Verdict.ACCEPTED if a_cont == b_cont else Verdict.WRONG

