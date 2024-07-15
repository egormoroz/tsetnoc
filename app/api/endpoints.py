from fastapi import APIRouter, HTTPException

from app.core.models import User, Problem

from app.core.models.content import PendingSub
from app.core.process import MalformedError
from app.infra.errors import AlreadyExists

from .schemas import AddedDTO, GetProblemDTO, NewProblemDTO, SubProcessResultDTO, NewSubmissionDTO
from .dependencies import Contests, Problems, SubProcessor, Submissions, Users


router = APIRouter()


@router.post("/register")
async def register_user(uname: str, users: Users):
    try:
        u = User.new(uname)
        users.add(u)
        return AddedDTO(id=u.id)
    except AlreadyExists:
        raise HTTPException(status_code=409, detail="User already exists")


@router.post("/join")
async def join_contest(uid: int, contest_id: int, conts: Contests):
    conts.add_participants([uid])


# TODO: bulk add
@router.post("/addproblem")
async def add_problem(prob_dto: NewProblemDTO, probs: Problems):
    prob = Problem(id=0, **prob_dto.__dict__)
    probs.add(prob)
    return AddedDTO(id=prob.id)


@router.post("/submit")
async def submit_answer(sub_dto: NewSubmissionDTO, sp: SubProcessor):
    sub = PendingSub(**sub_dto.__dict__)
    try:
        processed = sp.process(sub)
        return SubProcessResultDTO(id=processed.id, verdict=processed.verdict)
    except MalformedError as err:
        raise HTTPException(status_code=422, detail=f"Malformed submission: {err}")


# TODO: probably expose a better endpoint to get a list of names instead of raw ids?..
@router.get("/problems")
async def get_problemlist(uid: int, contest_id: int, conts: Contests):
    if not conts.has_participant(contest_id, uid):
        raise HTTPException(status_code=403, 
                            detail="The user can't see this problem list")
    return conts.get_problems(contest_id)


# TODO: bulk get
@router.get("/problem")
async def get_problem(uid: int, problem_id: int, probs: Problems):
    # TODO: test if uid is allowed to see this problem
    prob = probs.get(problem_id)
    if not prob:
        raise HTTPException(status_code=404, detail="Problem not found")
    # TODO: make sure this works, I haven't tested it yet lol
    return GetProblemDTO.model_validate(prob, from_attributes=True)


@router.get("/submissions")
async def get_submissions_list(
        uid: int, 
        by_problem: int|None,
        by_contest: int|None,
        subs: Submissions):
    raise NotImplementedError



