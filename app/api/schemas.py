from pydantic import BaseModel
from app.core.models import Verdict


class AddedDTO(BaseModel):
    id: int


class NewProblemDTO(BaseModel):
    name: str
    max_tries: int
    public: bool
    tags: set[int]
    content: str
    answer: str


class NewSubmissionDTO(BaseModel):
    author_id: int
    prob_id: int
    contest_id: int
    answer: str


class SubProcessResultDTO(BaseModel):
    id: int
    verdict: Verdict


class GetProblemDTO(BaseModel):
    id: int
    name: str
    max_tries: int
    public: bool
    tags: set[int]
    content: str
