import abc

from app.core.models import Problem, Submission, Contest
from app.core.models.user import User

class IUserRepo(abc.ABC):
    @abc.abstractmethod
    def add(self, user: User) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def has(self, id: int) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int) -> User | None:
        raise NotImplementedError


class IProblemRepo(abc.ABC):
    @abc.abstractmethod
    def add(self, problem: Problem) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def has(self, id: int) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int) -> Problem | None:
        raise NotImplementedError


class ISubRepo(abc.ABC):
    # 1. raises MalformedError of sorts if an error occurs
    # 2. fills the id field
    @abc.abstractmethod
    def add_checked(self, sub: Submission) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def has(self, id: int) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def count_tries(self, user_id: int, prob_id: int, cont_id: int) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int) -> Submission|None:
        raise NotImplementedError


class IContestRepo(abc.ABC):
    @abc.abstractmethod
    def add(self, contest: Contest) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def has(self, id: int) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def add_participants(self, ids: list[int]):
        raise NotImplementedError

    @abc.abstractmethod
    def add_problems(self, ids: list[int]):
        raise NotImplementedError

    @abc.abstractmethod
    def add_submissions(self, ids: list[int]):
        raise NotImplementedError

    @abc.abstractmethod
    def get_participants(self, id: int) -> list[int]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_problems(self, id: int) -> list[int]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_submissions(self, id: int) -> list[int]:
        raise NotImplementedError

    @abc.abstractmethod
    def has_participant(self, cont_id: int, user_id: int) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def has_problem(self, cont_id: int, prob_id: int) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def has_submission(self, cont_id: int, sub_id: int) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int) -> Contest | None:
        raise NotImplementedError

