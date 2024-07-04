import abc

from app.core.models import Problem, Submission

class IProblemRepo(abc.ABC):
    @abc.abstractmethod
    def add(self, problem: Problem):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int) -> Problem | None:
        raise NotImplementedError


class ISubRepo(abc.ABC):
    @abc.abstractmethod
    def add(self, sub: Submission):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int) -> Submission | None:
        raise NotImplementedError

