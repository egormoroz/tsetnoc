import enum

class ReservedTags(enum.Enum):
    # ignore the specified number 
    MAX_TRIES_UNLIMITED = 0
    ANS_CASE_INSENSETIVE = 1
    ANS_DONT_TRIM = 2
    # the problem isn't graded (no bonus/penalty for solving/failing)
    # can be used for problems with mistakes or for dummies/tests
    PROB_UNGRADED = 3

