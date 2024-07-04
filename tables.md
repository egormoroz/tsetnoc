## Tables
1. Problems
    - id (int)
    - name (fixed str)
    - content (str)
    - answer (str)

2. Tags
    - id (int)
    - name (fixed str)
    - description (optional, str)

3. ProblemTag
    - problem_id (int)
    - tag_id (int)


4. Users
    - id (int)
    - name (str)
    - login info
    - various stats (all ints)
        - n_submissions
        - probs_tried
        - probs_solved
        - etc


5. Submissions
    - id (int)
    - author_id (int)
    - answer (str)
    - verdict (enum):
        - ACCEPTED
        - WRONG
        - TRY_LIMIT_EXCEEDED 

