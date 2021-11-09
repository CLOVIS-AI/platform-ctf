import os
from subprocess import call

from flask import current_app
from flask_login import current_user
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String

from extensions import db
from .challenge_validation import ChallengeValidation

DEFAULT_VALID_SCRIPT_RETURN_CODE = 42


class ChallengeStep(db.Model):
    """Step of a challenge. Basic bloc for asking a user for a flag and
    validating it to receive some points.
    """

    id = Column(Integer, primary_key=True)
    section_id = Column(Integer,
                        ForeignKey("challenge_section.id"),
                        nullable=True)
    description = Column(String(120))
    points = Column(Integer, default=0)
    order = Column(Integer, default=0)
    validation_type = Column(String(32))
    validation_arg = Column(String(128))

    validations = relationship("ChallengeValidation", back_populates="step")

    __mapper_args__ = {
        "polymorphic_identity": "base",
        "polymorphic_on": validation_type,
    }

    def validate_submission_if_correct(self, submission):
        submission = submission.strip()
        if self.check_submission(submission):
            if not self.validated():
                ChallengeValidation(user=current_user, step=self).save()
            return {"status": "success"}
        return {"status": "failed"}

    def check_submission(self, submission):
        return False

    def validated(self):
        """Return whether the step has already been validated by `user`."""
        chall_val = ChallengeValidation.query.filter(
            ChallengeValidation.challenge_step_id == self.id,
            ChallengeValidation.user_id == current_user.id,
        ).one_or_none()
        return chall_val is not None


class StringChallengeStep(ChallengeStep):
    __mapper_args__ = {"polymorphic_identity": "string"}

    def check_submission(self, submission):
        return submission == self.validation_arg


class ScriptChallengeStep(ChallengeStep):
    """With this step, the flag submitted by the user is sent to a script.
    This lets the possibility to the author of a challenge to accept flags
    based on logic. The flag is considered valid if the return code of the
    challenge matched DEFAULT_VALID_SCRIPT_RETURN_CODE."""
    __mapper_args__ = {"polymorphic_identity": "script"}

    def check_submission(self, submission):
        script_file = os.path.join(
            current_app.config["CHALLENGE_DIR"],
            self.section.challenge.short_name,
            self.validation_arg,
        )
        retcode = call([script_file, submission])
        return retcode == DEFAULT_VALID_SCRIPT_RETURN_CODE


class DynamicChallengeStep(ChallengeStep):
    __mapper_args__ = {"polymorphic_identity": "dynamic"}

    def check_submission(self, submission):
        if current_user.instance.number is None:
            current_app.logger.debug("Error: no instance running")
            return False

        flag_file = os.path.join(
            current_app.config["BASE_INSTANCE_DATA"],
            str(current_user.instance.number),
            "flags",
            self.validation_arg,
        )

        if not os.path.isfile(flag_file):
            current_app.logger.debug(
                f"Error: the file '{flag_file}' does not exists")
            return False

        with open(flag_file, "r") as f:
            flag = f.readline().strip()

        return submission == flag


class FileChallengeStep(ChallengeStep):
    __mapper_args__ = {"polymorphic_identity": "file"}

    def check_submission(self, submission):
        flag_filename = os.path.join(
            current_app.config["CHALLENGE_DIR"],
            self.section.challenge.short_name,
            self.validation_arg,
        )
        with open(flag_filename, "r") as f:
            flag = f.readline().strip()

        return submission == flag


class FakeChallengeStep(ChallengeStep):
    """ChallengeStep that can be submitted without a flag. Used to validate sections."""
    __mapper_args__ = {"polymorphic_identity": "fakevalidation"}

    def check_submission(self, submission):
        return True
