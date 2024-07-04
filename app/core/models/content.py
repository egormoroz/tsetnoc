import enum
import dataclasses
from typing import Optional, Set

@dataclasses.dataclass(frozen=True)
class Answer:
    content: str


@dataclasses.dataclass
class Problem:
    id: int
    name: str

    max_tries: int
    # contest problems are private (not shown in global pool)
    public: bool

    tags: Set[int]
    # some sort of markdown probably
    content: str

    # attached images, plots, etc
    # attachments: Dict

    answer: Answer


class Verdict(enum.Enum):
    PENDING = 0
    ACCEPTED = 1
    WRONG = 2
    TRY_LIMIT_EXCEEDED = 3
    SUB_MALFORMED = 4


@dataclasses.dataclass
class Submission:
    id: Optional[int]

    author_id: int
    prob_id: int
    contest_id: Optional[int]

    n_try: int

    answer: Answer
    verdict: Verdict
