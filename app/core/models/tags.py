import enum
from pydantic import BaseModel


class Tag(BaseModel):
    id: int
    name: str|None = None
    description: str|None = None


class ReservedTags(enum.IntEnum):
    # ignore the specified number 
    MAX_TRIES_UNLIMITED = 0
    ANS_CASE_INSENSETIVE = 1
    ANS_DONT_TRIM = 2
    # the problem isn't graded (no bonus/penalty for solving/failing)
    # can be used for problems with mistakes or for dummies/tests
    PROB_UNGRADED = 3


    @classmethod
    def make(cls) -> list[Tag]:
        return [
            Tag(id=cls.MAX_TRIES_UNLIMITED, name="tries unlimited"),
            Tag(id=cls.ANS_CASE_INSENSETIVE, name="answer case insensetive"),
            Tag(id=cls.ANS_DONT_TRIM, name="answer not trimmed"),
            Tag(id=cls.PROB_UNGRADED, name="problem ungraded"),
        ]

