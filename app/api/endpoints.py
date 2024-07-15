from fastapi import APIRouter, HTTPException
import enum

from app.common.interfaces.composite import SubServerFB
from app.core.models import User, Problem, PendingSub
from app.common.errors import MalformedError, AlreadyExists

from .schemas import AddedDTO, GetProblemDTO, NewProblemDTO, SubProcessResultDTO, NewSubmissionDTO
from .dependencies import Contests, ProblemServer, Problems, SubProcessor, Submissions, Users


class ListFormat(enum.Enum):
    IDS = "ids"
    NAMES = "names"


router = APIRouter()


@router.post("/register")
async def register_user(uname: str, users: Users):
    try:
        u = User.new(uname)
        users.add(u)
        return AddedDTO(ids=[u.id])
    except AlreadyExists:
        raise HTTPException(status_code=409, detail="User already exists")


@router.post("/join")
async def join_contest(uid: int, contest_id: int, conts: Contests):
    conts.add_participants(contest_id, [uid])


@router.post("/addproblems")
async def add_problem(prob_dtos: list[NewProblemDTO], probs: Problems):
    ids = probs.add_many([Problem(id=0, **dto.__dict__) for dto in prob_dtos])
    return AddedDTO(ids=ids)


@router.post("/submit")
async def submit_answer(sub_dto: NewSubmissionDTO, sp: SubProcessor):
    sub = PendingSub(**sub_dto.__dict__)
    try:
        processed = sp.process(sub)
        return SubProcessResultDTO(id=processed.id, verdict=processed.verdict)
    except MalformedError as err:
        raise HTTPException(status_code=422, detail=f"Malformed submission: {err}")


@router.get("/problems")
async def get_problemlist(uid: int, contest_id: int, format: ListFormat, 
                          conts: Contests, probsrv: ProblemServer):
    if not conts.has_participant(contest_id, uid):
        raise HTTPException(status_code=403, 
                            detail="The user can't see this problem list")
    if format == ListFormat.IDS:
        return probsrv.get_ids(contest_id)
    else:
        return probsrv.get_names(contest_id)


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
async def get_submissionlist(
        uid: int, 
        by_problem: int|None,
        by_contest: int|None,
        subsrv: SubServerFB):
    return subsrv.get(uid, by_problem, by_contest)

