from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
import datetime
from typing import Annotated

from app.core.models import Verdict


intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
nestr = Annotated[str, mapped_column(String, nullable=False)]
nestr64 = Annotated[str, mapped_column(String(64), nullable=False)]
str64 = Annotated[str, mapped_column(String(64), nullable=True)]
int0 = Annotated[int, mapped_column(default=0)]

timestamp = Annotated[
    datetime.datetime,
    mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP()),
]

Base = declarative_base()


class ProblemTag(Base):
    __tablename__ = "problem_tag"
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)


class ContestProblem(Base):
    __tablename__ = "contest_problem"
    contest_id: Mapped[int] = mapped_column(ForeignKey("contests.id"), primary_key=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"), primary_key=True)



class ContestParticipant(Base):
    __tablename__ = "contest_participant"
    contest_id: Mapped[int] = mapped_column(ForeignKey("contests.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)


class Problem(Base):
    __tablename__ = "problems"

    id: Mapped[intpk]

    name: Mapped[nestr64]
    max_tries: Mapped[int] = mapped_column(nullable=False)
    content: Mapped[nestr]
    answer: Mapped[nestr64]

    tags = relationship("Tag", secondary="problem_tag", back_populates="problems")
    submissions = relationship('Submission', back_populates='problem')
    contests = relationship('Contest', secondary="contest_problem", back_populates='problems')


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[intpk]

    problems = relationship("Problem", secondary="problem_tag", back_populates="tags")
    info = relationship("TagInfo", back_populates="tag", uselist=False)


class TagInfo(Base):
    __tablename__ = "tag_info"

    id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)
    name: Mapped[nestr64]
    description : Mapped[str64]

    tag = relationship("Tag", back_populates="info")


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    name: Mapped[nestr64]
    n_submissions: Mapped[int0]
    probs_tried: Mapped[int0]
    probs_solved: Mapped[int0]

    submissions = relationship('Submission', back_populates='author')
    contests = relationship('Contest', secondary="contest_participant", 
                            back_populates='participants')


class Submission(Base):
    __tablename__ = 'submissions'

    id: Mapped[intpk]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    prob_id: Mapped[int]  = mapped_column(ForeignKey("problems.id"))
    contest_id: Mapped[int]  = mapped_column(ForeignKey("contests.id"))
    n_try: Mapped[int]
    answer: Mapped[nestr64]
    timestamp: Mapped[timestamp]
    verdict: Mapped[Verdict]

    author = relationship('User', back_populates='submissions')
    problem = relationship('Problem', back_populates='submissions')
    contest = relationship('Contest', back_populates='submissions')


class Contest(Base):
    __tablename__ = 'contests'

    id: Mapped[intpk]
    name: Mapped[nestr64]
    start: Mapped[datetime.datetime] = mapped_column(nullable=True)
    end: Mapped[datetime.datetime] = mapped_column(nullable=True)

    problems = relationship('Problem', secondary="contest_problem",
                            back_populates='contests')
    participants = relationship('User', secondary="contest_participant",
                                back_populates='contests')
    submissions = relationship('Submission', back_populates='contest')


