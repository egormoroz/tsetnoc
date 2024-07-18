from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.common.interfaces import IUserRepo, ISubRepo, IProblemRepo, IContestRepo
from app.infra.repos import (
    SQLUserRepo, SQLProblemRepo, SQLSubRepo, SQLContestRepo
)

# from app.settings import settings

class Bootstrap:
    _instance = None

    @staticmethod
    def instance():
        if Bootstrap._instance is None:
            Bootstrap._instance = Bootstrap()
        return Bootstrap._instance

    def __init__(self):
        self._engine = create_async_engine(
            # url=settings.DATABASE_URL_asyncpg,
            url="sqlite+aiosqlite:///test.db"
        )
        self._session = async_sessionmaker(self._engine)

        self._users = SQLUserRepo(self._session)
        self._problems = SQLProblemRepo(self._session)
        self._subs = SQLSubRepo(self._session)
        self._conts = SQLContestRepo(self._session)

    @property
    def users(self) -> IUserRepo:
        return self._users

    @property
    def problems(self) -> IProblemRepo:
        return self._problems

    @property
    def subs(self) -> ISubRepo:
        return self._subs

    @property
    def contests(self) -> IContestRepo:
        return self._conts
