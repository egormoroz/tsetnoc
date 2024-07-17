from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    ForeignKey, Column, Integer, String, Table, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from typing import Annotated

from app.core.models import Verdict


intpk = Annotated[int, mapped_column(primary_key=True)]
nestr = Annotated[str, mapped_column(String, nullable=False)]
nestr64 = Annotated[str, mapped_column(String(64), nullable=False)]
str64 = Annotated[str, mapped_column(String(64), nullable=True)]
int0 = Annotated[int, mapped_column(default=0)]

timestamp = Annotated[
    datetime.datetime,
    mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP()),
]

Base = declarative_base()


problem_tag = Table("problem_tag", Base.metadata,
    Column("problem_id", Integer, ForeignKey("problems.id")),
    Column("tag_id", Integer, ForeignKey("tags.id"))
)


contest_problem = Table('contest_problem', Base.metadata,
    Column('contest_id', Integer, ForeignKey('contests.id')),
    Column('problem_id', Integer, ForeignKey('problems.id'))
)

contest_participant = Table('contest_participant', Base.metadata,
    Column('contest_id', Integer, ForeignKey('contests.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)


class Problem(Base):
    __tablename__ = "problems"

    id: Mapped[intpk]

    name: Mapped[nestr64]
    max_tries: Mapped[int] = mapped_column(nullable=False)
    content: Mapped[nestr]
    answer: Mapped[nestr64]

    tags = relationship("Tag", secondary=problem_tag, back_populates="problems")
    submissions = relationship('Submission', back_populates='problem')
    contests = relationship('Contest', secondary=contest_problem, back_populates='problems')


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[intpk]
    name: Mapped[nestr64]
    description : Mapped[str64]

    problems = relationship("Problem", secondary=problem_tag, back_populates="tags")


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    name: Mapped[nestr64]
    n_submissions: Mapped[int0]
    probs_tried: Mapped[int0]
    probs_solved: Mapped[int0]

    submissions = relationship('Submission', back_populates='author')
    contests = relationship('Contest', secondary=contest_participant, back_populates='participants')


class Submission(Base):
    __tablename__ = 'submissions'

    id: Mapped[intpk]
    author_id: Mapped[int] = mapped_column(ForeignKey("users'id"))
    prob_id: Mapped[int]  = mapped_column(ForeignKey("problems'id"))
    contest_id: Mapped[int]  = mapped_column(ForeignKey("contests'id"))
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
    start: Mapped[datetime.datetime] = mapped_column(nullable=False)
    end: Mapped[datetime.datetime] = mapped_column(nullable=False)

    problems = relationship('Problem', secondary=contest_problem, back_populates='contests')
    participants = relationship('User', secondary=contest_participant, back_populates='contests')
    submissions = relationship('Submission', back_populates='contest')


