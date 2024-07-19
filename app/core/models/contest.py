from pydantic import BaseModel
from datetime import datetime

class Contest(BaseModel):
    id: int
    name: str
    start: datetime|None = None
    end: datetime|None = None
