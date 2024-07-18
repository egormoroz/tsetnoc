import dataclasses

@dataclasses.dataclass
class User:
    name: str
    
    n_submissions: int
    probs_tried: int
    probs_solved: int

    id: int|None = None

    @staticmethod
    def new(name: str):
        return User(name=name, probs_tried=0, probs_solved=0, n_submissions=0)

