from app.common.interfaces import IUserRepo, ISubRepo, IProblemRepo, IContestRepo


class Bootstrap:
    _instance = None

    @staticmethod
    def instance():
        if Bootstrap._instance is None:
            Bootstrap._instance = Bootstrap()
        return Bootstrap._instance

    def __init__(self):
        # init everything
        pass

    @property
    def users(self) -> IUserRepo:
        raise NotImplementedError

    @property
    def problems(self) -> IProblemRepo:
        raise NotImplementedError

    @property
    def subs(self) -> ISubRepo:
        raise NotImplementedError

    @property
    def contests(self) -> IContestRepo:
        raise NotImplementedError
