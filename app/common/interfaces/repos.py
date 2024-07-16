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

    @abc.abstractmethod
    def can_see_problem(self, uid: int, pid: int) -> bool:
        raise NotImplementedError


class IProblemRepo(abc.ABC):
    @abc.abstractmethod
    def add(self, problem: Problem) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def add_many(self, problems: list[Problem]) -> list[int]:
        raise NotImplementedError

    @abc.abstractmethod
    def has(self, id: int) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int) -> Problem | None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_ids_by_contest(self, cont_id: int) -> list[int]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_contest(self, cont_id: int) -> list[Problem]:
        raise NotImplementedError


class ISubRepo(abc.ABC):
    # 1. raises MalformedError of sorts if an error occurs
    # 2. fills the id field
    @abc.abstractmethod
    def add_checked(self, sub: Submission) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def count_tries(self, user_id: int, prob_id: int, cont_id: int) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int) -> Submission|None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_ids_by(self, uid: int, pid: int|None, cid: int|None) -> list[int]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by(self, uid: int, pid: int|None, cid: int|None) -> list[Submission]:
        raise NotImplementedError


class IContestRepo(abc.ABC):
    @abc.abstractmethod
    def add(self, contest: Contest) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def has(self, id: int) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def add_participants(self, cid: int, uids: list[int]):
        raise NotImplementedError

    @abc.abstractmethod
    def add_problems(self, cid: int, pids: list[int]):
        raise NotImplementedError

    @abc.abstractmethod
    def get_participants(self, cid: int) -> list[int]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_problems(self, cid: int) -> list[int]:
        raise NotImplementedError

    @abc.abstractmethod
    def has_participant(self, cont_id: int, user_id: int) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def has_problem(self, cont_id: int, prob_id: int) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int) -> Contest | None:
        raise NotImplementedError


# e.g. the whole db
# might be unnecessary tbqh
class IOmniRepo(abc.ABC):
    @property
    @abc.abstractmethod
    def users(self) -> IUserRepo:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def problems(self) -> IProblemRepo:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def submissions(self) -> ISubRepo:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def contests(self) -> IContestRepo:
        raise NotImplementedError

