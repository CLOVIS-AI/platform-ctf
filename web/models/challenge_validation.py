from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey, Column
from sqlalchemy.types import Integer

from extensions import db


class ChallengeValidation(db.Model):
    """Relation between a ChallengeStep and a User. """

    challenge_step_id = Column(
        Integer, ForeignKey("challenge_step.id"), primary_key=True
    )
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)

    user = relationship("User", back_populates="validations")
    step = relationship("ChallengeStep", back_populates="validations")
