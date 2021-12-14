from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey, Column
from sqlalchemy.types import Integer, String

from .challenge import Challenge
from ..extensions import db


class ChallengeSection(db.Model):
    """
    A section of a challenge, with a title and a description.

    A section is composed of multiple steps, which describe how the user can prove that they completed that section.
    """

    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    description = Column(String(1024000))
    chall_id = Column(Integer, ForeignKey(Challenge.id))
    order = Column(Integer)
    steps = relationship("ChallengeStep", backref="section")
