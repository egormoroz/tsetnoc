from typing import Set

from app.infra.interfaces import IProblemRepo, ISubRepo
from .models import Submission, Verdict, Answer, ReservedTags


# hypothetically, can be an interface (but why?)
class SubProcessor:
    def __init__(self, problems: IProblemRepo, submissions: ISubRepo):
        self._probs = problems
        self._subs = submissions

    # TODO: should we add the submission to the table here or outside?
    def process(self, sub: Submission) -> Verdict:
        prob = self._probs.get(sub.prob_id)
        if prob is None:
            return Verdict.SUB_MALFORMED
        if not (sub.id is None and sub.verdict == Verdict.PENDING):
            return Verdict.SUB_MALFORMED

        if ReservedTags.MAX_TRIES_UNLIMITED not in prob.tags \
                and sub.n_try > prob.max_tries:
            return Verdict.TRY_LIMIT_EXCEEDED

        return compare_answers(sub.answer, prob.answer, prob.tags)


def compare_answers(a: Answer, b: Answer, tags: Set[int]) -> Verdict:
    a_cont, b_cont = a.content, b.content

    if ReservedTags.ANS_DONT_TRIM not in tags:
        a_cont, b_cont = a_cont.strip(), b_cont.strip()
    if ReservedTags.ANS_CASE_INSENSETIVE in tags:
        a_cont, b_cont = a_cont.lower(), b_cont.lower()

    return Verdict.ACCEPTED if a_cont == b_cont else Verdict.WRONG
