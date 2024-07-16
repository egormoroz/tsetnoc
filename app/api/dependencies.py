from app.common.interfaces import (
    IContestRepo, IProblemRepo, ISubRepo, IUserRepo,
)

from app.bootstrap import Bootstrap as _Bootstrap

from app.core.process import SubProcessor as _SubProcessor

from fastapi import Depends
from typing import Annotated


Bootstrap = Annotated[_Bootstrap, Depends(_Bootstrap.instance)]


def getter(attr_name: str):
    def fn(bs: _Bootstrap):
        return getattr(bs, attr_name)
    return fn

def get_subprocessor(bs: Bootstrap) -> _SubProcessor:
    return _SubProcessor(bs.users, bs.problems, bs.subs)


Users = Annotated[IUserRepo, Depends(getter("users"))]
Problems = Annotated[IProblemRepo, Depends(getter("problems"))]
Submissions = Annotated[ISubRepo, Depends(getter("subs"))]
Contests = Annotated[IContestRepo, Depends(getter("contests"))]
SubProcessor = Annotated[_SubProcessor, Depends(get_subprocessor)]

