from app.infra.interfaces import IProblemRepo, ISubRepo, IContestRepo, IUserRepo
from .models import PendingSub, Submission, Verdict, Answer, ReservedTags

import enum

class ErrorCode(enum.IntEnum):
    PROBLEM_NOT_FOUND = 0
    USER_NOT_FOUND = 1


class MalformedError(Exception):
    def __init__(self, ec: ErrorCode):
        super().__init__()
        self.ec = ec


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

    def process(self, sub: PendingSub) -> Submission:
        prob = self._probs.get(sub.prob_id)
        if prob is None:
            raise MalformedError(ErrorCode.PROBLEM_NOT_FOUND)

        n_try = 1 + self._subs.count_tries(
                sub.author_id, sub.prob_id, sub.contest_id)

        if ReservedTags.MAX_TRIES_UNLIMITED not in prob.tags \
                and n_try > prob.max_tries:
            verdict = Verdict.TRY_LIMIT_EXCEEDED
        else:
            verdict = self._compare_answers(sub.answer, prob.answer, prob.tags)

        res = sub.finalize(n_try, verdict)
        self._subs.add_checked(res) # assigns the id or raises MalformedError
        return res


    @staticmethod
    def _compare_answers(a: Answer, b: Answer, tags: set[int]) -> Verdict:
        a_cont, b_cont = a.content, b.content

        if ReservedTags.ANS_DONT_TRIM not in tags:
            a_cont, b_cont = a_cont.strip(), b_cont.strip()
        if ReservedTags.ANS_CASE_INSENSETIVE in tags:
            a_cont, b_cont = a_cont.lower(), b_cont.lower()

        return Verdict.ACCEPTED if a_cont == b_cont else Verdict.WRONG


