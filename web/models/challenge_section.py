from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey, Column
from sqlalchemy.types import Integer, String

from extensions import db
from .challenge import Challenge


class ChallengeSection(db.Model):
    """Subsection of a challenge. Basic block containing instructions and possibly steps."""

    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    description = Column(String(1024000))
    chall_id = Column(Integer, ForeignKey(Challenge.id))
    order = Column(Integer)
    steps = relationship("ChallengeStep", backref="section")
