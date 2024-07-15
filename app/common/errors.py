import enum


class ErrorCode(enum.IntEnum):
    PROBLEM_NOT_FOUND = 0
    USER_NOT_FOUND = 1
    CONTEST_NOT_FOUND = 2


class MalformedError(Exception):
    def __init__(self, ec: ErrorCode):
        super().__init__()
        self.ec = ec


class AlreadyExists(Exception):
    pass
