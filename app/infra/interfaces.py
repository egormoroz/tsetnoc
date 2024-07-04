import abc

from typing import List, Optional
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
    @abc.abstractmethod
    def add(self, sub: Submission) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def has(self, id: int) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def count_tries(self, user_id: int, prob_id: int, 
                    cont_id: Optional[int]) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int) -> Submission | None:
        raise NotImplementedError


class IContestRepo(abc.ABC):
    @abc.abstractmethod
    def add(self, contest: Contest) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def has(self, id: int) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def add_participants(self, ids: List[int]):
        raise NotImplementedError

    @abc.abstractmethod
    def add_problems(self, ids: List[int]):
        raise NotImplementedError

    @abc.abstractmethod
    def add_submissions(self, ids: List[int]):
        raise NotImplementedError

    @abc.abstractmethod
    def get_participants(self, id: int) -> List[int]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_problems(self, id: int) -> List[int]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_submissions(self, id: int) -> List[int]:
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

