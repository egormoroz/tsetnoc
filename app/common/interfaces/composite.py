# Implementations of various complex queries that might require some optimization

import abc
from typing import override
from .repos import IProblemRepo, IContestRepo

# IUserServer serves users (for leaderboards)

class IProblemServer(abc.ABC):
    @abc.abstractmethod
    def get_ids(self, cid: int) -> list[int]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_names(self, cid: int) -> list[str]:
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


