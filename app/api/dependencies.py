from app.common.interfaces import (
    IContestRepo, IOmniRepo, IProblemRepo, ISubRepo, IUserRepo,
    IProblemServer, ProblemServerFB
)

from app.common.interfaces.composite import ISubServer, SubServerFB
from app.core.process import SubProcessor as _SubProcessor

from fastapi import Depends
from typing import Annotated

async def get_omni() -> IOmniRepo:
    # e.g. return sqlalchemy session wrapper
    raise NotImplementedError


OmniRepo = Annotated[IOmniRepo, Depends(get_omni)]

async def get_users(omni: OmniRepo) -> IUserRepo:
    return omni.users

async def get_probs(omni: OmniRepo) -> IProblemRepo:
    return omni.problems

async def get_subs(omni: OmniRepo) -> ISubRepo:
    return omni.submissions

async def get_contests(omni: OmniRepo) -> IContestRepo:
    return omni.contests

# TODO
async def get_probserver(omni: OmniRepo) -> IProblemServer:
    return ProblemServerFB(omni.problems, omni.contests)

# TODO
async def get_subserver(omni: OmniRepo) -> ISubServer:
    return SubServerFB(omni.submissions)

async def get_subprocessor(omni: OmniRepo) -> _SubProcessor:
    return _SubProcessor(omni.users, omni.problems, omni.submissions, omni.contests)

Users = Annotated[IUserRepo, Depends(get_users)]
Problems = Annotated[IProblemRepo, Depends(get_probs)]
Submissions = Annotated[ISubRepo, Depends(get_subs)]
Contests = Annotated[IContestRepo, Depends(get_contests)]
SubProcessor = Annotated[_SubProcessor, Depends(get_subprocessor)]
ProblemServer = Annotated[IProblemServer, Depends(get_probserver)]
SubServer = Annotated[ISubServer, Depends(get_subserver)]

