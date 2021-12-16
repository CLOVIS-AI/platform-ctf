from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String

from ..extensions import db


class Challenge(db.Model):
    """
    Scenarios, challenges, documentation pages are all modeled by this class.

    A challenge is split into sections, themselves split into steps.
    Each section has a title, a description and one or more validation steps.
    A step corresponds to a requested flag.
    """

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    short_name = Column(String(8), unique=True, nullable=False)
    description = Column(String(1024000))
    category = Column(String(32), default="Misc")
    author = Column(String(64), default="Anonymous")

    sections = relationship("ChallengeSection", backref="challenge")
    resource = relationship("ChallengeResource", uselist=False, back_populates="challenge")

    @property
    def points(self):
        from . import ChallengeStep, ChallengeSection
        return db.session.query(func.sum(ChallengeStep.points)).join(ChallengeStep.section).filter(
            ChallengeSection.challenge == self).first()[0]
