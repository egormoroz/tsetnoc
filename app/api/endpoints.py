from fastapi import FastAPI, HTTPException
import enum
from loguru import logger

from app.core.models import User, Problem, PendingSub
from app.common.errors import MalformedError, AlreadyExists

from .schemas import GetProblemDTO, NewProblemDTO, SubProcessResultDTO, NewSubmissionDTO
from .dependencies import Contests, Problems, SubProcessor, Submissions, Users


class ProbListFmt(enum.Enum):
    IDS = "ids"
    IDS_NAMES = "ids_names"
    FULL = "full"


class SubListFmt(enum.Enum):
    IDS = "ids"
    FULL = "full"


app = FastAPI()


@app.post("/register")
async def register_user(uname: str, users: Users):
    try:
        u = User.new(uname)
        await users.add(u)
        logger.info(f"created user {u}")
        return {"message": "user created successfully", "id": f"{u.id}"}
    except AlreadyExists:
        raise HTTPException(status_code=409, detail="User already exists")


@app.post("/join")
async def join_contest(uid: int, contest_id: int, conts: Contests):
    try:
        await conts.add_participants(contest_id, [uid])
        logger.info(f"user(id={uid}) joined contest(id={contest_id})")
        return {"message": "joined contest successfully"}
    except MalformedError as e:
        logger.error(f"user(id={uid}) failed to joined contest(id={contest_id}): ",
                     "either user or contest doesn't exist: ", e.ec)
        raise HTTPException(status_code=422, detail="user/contest doesn't exist")


@app.post("/problems", status_code=201)
async def add_problems(prob_dtos: list[NewProblemDTO], probs: Problems):
    core_probs = [Problem(id=0, **dto.__dict__) for dto in prob_dtos]
    ids = await probs.add_many(core_probs)
    logger.info("added problems: {}".format(", ".join(
        f"Prob(id={p.id}, name={p.name})" for p in core_probs
    )))
    return {"message": "problems added successfully", "ids": ids }


@app.post("/contest/{cid}/problems", status_code=201)
async def add_probs_to_contest(cid: int, prob_ids: list[int], conts: Contests):
    try:
        await conts.add_problems(cid, prob_ids)
        logger.info(f"added {prob_ids=} to contest(id={cid})")
        return {"message": "problems added to contest successfully" }
    except MalformedError:
        logger.error(f"failed to add problems to contest(id={cid}): ",
                     "the contest doesn't exist")
        raise HTTPException(status_code=422, detail="contest doesn't exist")


@app.post("/submit")
async def submit_answer(sub_dto: NewSubmissionDTO, sp: SubProcessor):
    sub = PendingSub(**sub_dto.__dict__)
    try:
        processed = await sp.process(sub)
        logger.info(f"processed sub(id={processed.id})")
        return SubProcessResultDTO(id=processed.id, verdict=processed.verdict)
    except MalformedError as err:
        logger.error(f"received malformed submission: {err}")
        raise HTTPException(status_code=422, detail=f"Malformed submission: {err}")


@app.get("/problems")
async def get_problem_list(
    uid: int,
    contest_id: int,
    fmt: ProbListFmt,
    users: Users, probs: Problems
):
    if not await users.joined_contest(uid, contest_id):
        logger.error(f"user(id={uid}) tried to sneak a peek",
                     f"contest(id={contest_id}) problem list")
        raise HTTPException(status_code=403, 
                            detail="The user can't see this problem list")
    logger.info(f"user(id={uid}) requested problem list for ",
                f"contest(id={contest_id})")
    if fmt == ProbListFmt.IDS:
        return probs.get_ids_by_contest(contest_id)
    elif fmt == ProbListFmt.IDS_NAMES:
        return [{"id": p.id, "name": p.name}
                for p in await probs.get_by_contest(contest_id)]
    else:
        assert fmt == ProbListFmt.FULL
        return [GetProblemDTO.model_validate(p, from_attributes=True)
                for p in await probs.get_by_contest(contest_id)]


@app.get("/problem")
async def get_problem(uid: int, problem_id: int, probs: Problems, users: Users):
    # also checks if the problem exists, since you cannot see a nonexistant problem lol
    if not await users.can_see_problem(uid, problem_id):
        logger.error(f"user(id={uid}) troid to see problem(id={problem_id})")
        raise HTTPException(status_code=403, detail="The user either can't see "
            + "this problem or the problem doesn't exist")
    logger.info(f"user(id={uid}) requested problem(id={problem_id})")
    prob = probs.get(problem_id)
    return GetProblemDTO.model_validate(prob, from_attributes=True)


@app.get("/submissions")
async def get_submission_list(
    uid: int, 
    by_problem: int|None,
    by_contest: int|None,
    fmt: SubListFmt,
    subs: Submissions
):
    logger.info(f"user(id={uid}) requested submission list, filtered ",
                f"{by_problem=}, {by_contest}")
    if fmt == SubListFmt.IDS:
        return await subs.get_ids_by(uid, by_problem, by_contest)
    else:
        assert fmt == SubListFmt.FULL
        return await subs.get_by(uid, by_problem, by_contest)


@app.get("/contests")
async def get_contest_list(conts: Contests):
    logger.info("requested contest list")
    return await conts.all()


@app.get("/users")
async def get_user_list(users: Users):
    logger.info("requested user list")
    return await users.all()

@app.get("/contest/{cid}/users")
async def get_contest_users(cid: int, users: Users):
    logger.info(f"requested user list from contest(id={cid})")
    return await users.get_ids_by_contest(cid)

