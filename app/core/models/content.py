import enum
from dataclasses import dataclass


@dataclass
class Problem:
    id: int
    name: str

    max_tries: int
    # contest problems are private (not shown in global pool)
    tags: set[int]
    # some sort of markdown probably
    content: str

    # attached images, plots, etc
    # attachments: Dict

    answer: str


class Verdict(enum.IntEnum):
    ACCEPTED = 0
    WRONG = 1
    TRY_LIMIT_EXCEEDED = 2


@dataclass
class RawSub:
    author_id: int
    prob_id: int
    contest_id: int

    answer: str


@dataclass
class Submission(RawSub):
    id: int
    n_try: int
    verdict: Verdict


@dataclass
class PendingSub(RawSub):
    def finalize(self, n_try: int, verdict: Verdict) -> Submission:
        return Submission(
            author_id=self.author_id,
            prob_id=self.prob_id,
            contest_id=self.contest_id,
            answer=self.answer,
            n_try=n_try,
            verdict=verdict,
            id=0)
