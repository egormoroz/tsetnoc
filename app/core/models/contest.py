import dataclasses
from typing import List

@dataclasses.dataclass
class Contest:
    id: int
    particip_ids: List[int]
    prob_ids: List[int]
    sub_ids: List[int]

