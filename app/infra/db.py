from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    ForeignKey, Column, Integer, String, Table, Enum, Date, DateTime
)
from sqlalchemy.orm import relationship

import enum
import datetime


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

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    max_tries = Column(Integer, nullable=False)
    content = Column(String, nullable=False)
    answer = Column(String(64), nullable=False)

    tags = relationship("Tag", secondary=problem_tag, back_populates="problems")
    submissions = relationship('Submission', back_populates='problem')
    contests = relationship('Contest', secondary=contest_problem, back_populates='problems')



class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    description = Column(String(64), nullable=True)

    problems = relationship("Problem", secondary=problem_tag, back_populates="tags")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    n_submissions = Column(Integer, default=0)
    probs_tried = Column(Integer, default=0)
    probs_solved = Column(Integer, default=0)

    submissions = relationship('Submission', back_populates='author')
    contests = relationship('Contest', secondary=contest_participant, back_populates='participants')


class Verdict(enum.IntEnum):
    ACCEPTED = 0
    WRONG = 1
    TRY_LIMIT_EXCEEDED = 2


class Submission(Base):
    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    prob_id = Column(Integer, ForeignKey('problems.id'))
    contest_id = Column(Integer, ForeignKey('contests.id'))
    answer = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    verdict = Column(Enum(Verdict))

    author = relationship('User', back_populates='submissions')
    problem = relationship('Problem', back_populates='submissions')
    contest = relationship('Contest', back_populates='submissions')


class Contest(Base):
    __tablename__ = 'contests'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    start = Column(Date, nullable=False)
    end = Column(Date, nullable=False)

    problems = relationship('Problem', secondary=contest_problem, back_populates='contests')
    participants = relationship('User', secondary=contest_participant, back_populates='contests')
    submissions = relationship('Submission', back_populates='contest')


