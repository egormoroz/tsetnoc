import enum


class ErrorCode(enum.IntEnum):
    # unsure how to find out which key exactly was incorrect
    FOREIGN_KEY_ERROR = 0

    PROBLEM_NOT_FOUND = 1
    USER_NOT_FOUND = 2
    CONTEST_NOT_FOUND = 3
    TAG_NOT_FOUND = 4


# TOOD: better name
class MalformedError(Exception):
    def __init__(self, ec: ErrorCode=ErrorCode.FOREIGN_KEY_ERROR):
        super().__init__()
        self.ec = ec


class AlreadyExists(Exception):
    pass
