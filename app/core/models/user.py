import dataclasses

@dataclasses.dataclass
class User:
    id: int
    name: str
    
    probs_tried: int
    probs_solved: int

    @staticmethod
    def new(name: str):
        return User(id=0, name=name, probs_tried=0, probs_solved=0)

