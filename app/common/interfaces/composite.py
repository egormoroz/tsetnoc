# Implementations of various complex queries that might require some optimization

import abc
from typing import override

from app.core.models.content import Submission
from .repos import IProblemRepo, IContestRepo, ISubRepo

# IUserServer serves users (for leaderboards)

class IProblemServer(abc.ABC):
    @abc.abstractmethod
    def get_ids(self, cid: int) -> list[int]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_names(self, cid: int) -> list[str]:
        raise NotImplementedError



class ISubServer(abc.ABC):
    @abc.abstractmethod
    def get(self, by_uid: int, by_prob: int|None, by_cont: int|None) -> list[Submission]:
        raise NotImplementedError


# Fallback implementations

class ProblemServerFB(IProblemServer):
    def __init__(self, probs: IProblemRepo, conts: IContestRepo):
        super().__init__()
        self._probs = probs
        self._conts = conts

    @override
    def get_ids(self, cid: int) -> list[int]:
        return self._conts.get_problems(cid)

    @override
    def get_names(self, cid: int) -> list[str]:
        ids = self._conts.get_problems(cid)
        return [self._probs.get(i).name for i in ids]


class SubServerFB(ISubServer):
    def __init__(self, subs: ISubRepo):
        self._subs = subs

    @override
    def get(self, by_uid: int, by_prob: int|None, by_cont: int|None) -> list[Submission]:
        def subfilter(sub: Submission):
            by_cont = by_prob or sub.prob_id
            return (by_prob or sub.prob_id) == sub.prob_id \
                    and (by_cont or sub.contest_id) == sub.contest_id
        return [sub for sub in self._subs.get_by(by_uid) if subfilter(sub)]

