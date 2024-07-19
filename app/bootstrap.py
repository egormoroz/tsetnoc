from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.common.interfaces import IUserRepo, ISubRepo, IProblemRepo, IContestRepo
from app.infra.models import Base
from app.infra.repos import (
    SQLUserRepo, SQLProblemRepo, SQLSubRepo, SQLContestRepo
)

# from app.settings import settings

class Bootstrap:
    _instance = None

    @staticmethod
    async def instance():
        if Bootstrap._instance is None:
            Bootstrap._instance = Bootstrap()
            async with Bootstrap._instance._engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)

        return Bootstrap._instance

    def __init__(self):
        self._engine = create_async_engine(
            # url=settings.DATABASE_URL_asyncpg,
            url="sqlite+aiosqlite:///test.db",
            echo=True
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


# for quick testing I use sqlite, and it doesn't check 
# for foreign key constraints by default
from sqlalchemy import event
from sqlalchemy.pool import Pool

@event.listens_for(Pool, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
