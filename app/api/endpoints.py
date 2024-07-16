from fastapi import APIRouter, HTTPException
import enum

from app.core.models import User, Problem, PendingSub
from app.common.errors import MalformedError, AlreadyExists

from .schemas import AddedDTO, GetProblemDTO, NewProblemDTO, SubProcessResultDTO, NewSubmissionDTO
from .dependencies import Contests, Problems, SubProcessor, Submissions, Users


class ProbListFmt(enum.Enum):
    IDS = "ids"
    IDS_NAMES = "ids_names"
    FULL = "full"


class SubListFmt(enum.Enum):
    IDS = "ids"
    FULL = "full"


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
async def get_problem_list(
        uid: int,
        contest_id: int,
        fmt: ProbListFmt,
        conts: Contests, probs: Problems):
    if not conts.has_participant(contest_id, uid):
        raise HTTPException(status_code=403, 
                            detail="The user can't see this problem list")
    if fmt == ProbListFmt.IDS:
        return probs.get_ids_by_contest(contest_id)
    elif fmt == ProbListFmt.IDS_NAMES:
        return [{"id": p.id, "name": p.name}
                for p in probs.get_by_contest(contest_id)]
    else:
        assert fmt == ProbListFmt.FULL
        return [GetProblemDTO.model_validate(p, from_attributes=True)
                for p in probs.get_by_contest(contest_id)]


@router.get("/problem")
async def get_problem(uid: int, problem_id: int, probs: Problems, users: Users):
    # also checks if the problem exists, since you cannot see a nonexistant problem lol
    if not users.can_see_problem(uid, problem_id):
        raise HTTPException(status_code=403, detail="The user either can't see "
            + "this problem or the problem does'nt exist")
    prob = probs.get(problem_id)
    return GetProblemDTO.model_validate(prob, from_attributes=True)


@router.get("/submissions")
async def get_submissionlist(
        uid: int, 
        by_problem: int|None,
        by_contest: int|None,
        fmt: SubListFmt,
        subs: Submissions):
    if fmt == SubListFmt.IDS:
        return subs.get_ids_by(uid, by_problem, by_contest)
    else:
        assert fmt == SubListFmt.FULL
        return subs.get_by(uid, by_problem, by_contest)


