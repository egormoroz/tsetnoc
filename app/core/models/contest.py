import dataclasses

@dataclasses.dataclass
class Contest:
    id: int
    name: str
    particip_ids: list[int]
    prob_ids: list[int]
    sub_ids: list[int]

