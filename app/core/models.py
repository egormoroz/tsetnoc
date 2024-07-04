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
    n_try: int

    answer: Answer
    verdict: Verdict


@dataclasses.dataclass
class User:
    id: int
    name: str
    
    probs_tried: int
    probs_solved: int

