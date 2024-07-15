import dataclasses

@dataclasses.dataclass
class User:
    id: int
    name: str
    
    probs_tried: int
    probs_solved: int

