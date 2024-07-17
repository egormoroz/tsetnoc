import dataclasses
from datetime import datetime

@dataclasses.dataclass
class Contest:
    id: int
    name: str
    start: datetime|None = None
    end: datetime|None = None
