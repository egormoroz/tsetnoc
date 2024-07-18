import abc

from app.core.models import Problem, Submission, Contest, User, Tag

class IUserRepo(abc.ABC):
    @abc.abstractmethod
    async def add(self, user: User) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, id: int) -> User | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def can_see_problem(self, uid: int, pid: int) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_ids_by_contest(self, cont_id: int) -> list[int]:
        raise NotImplementedError

    @abc.abstractmethod
    async def joined_contest(self, uid: int, cid: int) -> bool:
        raise NotImplementedError


class IProblemRepo(abc.ABC):
    @abc.abstractmethod
    async def add_many(self, problems: list[Problem]) -> list[int]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, id: int) -> Problem | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_ids_by_contest(self, cont_id: int) -> list[int]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_contest(self, cont_id: int) -> list[Problem]:
        raise NotImplementedError


class ITagRepo(abc.ABC):
    @abc.abstractmethod
    async def add_many(self, tags: list[Tag], keep_ids=False) -> list[int]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_many(self, ids: list[int]) -> list[Tag]:
        raise NotImplementedError


class ISubRepo(abc.ABC):
    # 1. raises MalformedError of sorts if an error occurs
    # 2. fills the id field
    @abc.abstractmethod
    async def add_checked(self, sub: Submission) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    async def count_tries(self, user_id: int, prob_id: int, cont_id: int) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_ids_by(self, uid: int, pid: int|None, cid: int|None) -> list[int]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by(self, uid: int, pid: int|None, cid: int|None) -> list[Submission]:
        raise NotImplementedError


class IContestRepo(abc.ABC):
    @abc.abstractmethod
    async def add(self, contest: Contest) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    async def add_participants(self, cid: int, uids: list[int]):
        raise NotImplementedError

    @abc.abstractmethod
    async def add_problems(self, cid: int, pids: list[int]):
        raise NotImplementedError

