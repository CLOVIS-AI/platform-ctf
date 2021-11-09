import os
from datetime import datetime, timedelta
from shutil import copytree, rmtree
from subprocess import CalledProcessError

from flask import current_app
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import DateTime, Integer, String

from extensions import db
from terraform_client import TerraformClient, TerraformError


class ResourceInstance(db.Model):
    """Object that represent the instanciation of a ChallengeResource object."""

    id = Column(Integer, primary_key=True)
    type = Column(String(64))
    user_id = Column(Integer, ForeignKey("user.id"))
    challenge_resource_id = Column(Integer, ForeignKey("challenge_resource.id"))
    status = Column(String(200))
    message = Column(String(200))
    expiration = Column(DateTime)
    number = Column(Integer, default=-1)

    user = relationship(
        "User", uselist=False, back_populates="instance", foreign_keys=user_id
    )
    resource = relationship("ChallengeResource", back_populates="instances")

    __mapper_args__ = {
        "polymorphic_identity": "resource", "polymorphic_on": type}

    def start(self):
        if self.started:
            return self.to_dict()

        try:
            self.status = "starting"
            self.message = None
            self.number = self.get_new_instance_number()
            self.save()

            if self.number < 0:
                return self.fail_with_message(
                    "The maximum number of running instances has been reached."
                )

            copytree(
                os.path.join(
                    current_app.config["CHALLENGE_DIR"],
                    self.resource.challenge.short_name,
                    "instance",
                ),
                os.path.join(
                    current_app.config["BASE_INSTANCE_DATA"], str(self.number)
                ),
            )

            provision_result_data = self.provide()

            self.status = "started"
            self.message = self.resource.args.format(**provision_result_data)
            expiration_time_seconds = current_app.config["INSTANCE_EXPIRATION_TIME"] - 2
            self.expiration = datetime.now() + timedelta(
                seconds=expiration_time_seconds
            )
            self.save()
            return self.to_dict()
        except Exception as e:
            current_app.logger.error(e)
            return self.fail_with_message("Something went wrong.")

    def provide(self):
        return {}

    def status_as_dict(self):
        return self.to_dict()

    def stop(self):
        if self.stopped:
            return self.to_dict()

        self.status = "stopping"
        self.message = None
        self.save()

        try:
            self.destroy()
            self.remove_instance_folder_if_necessary()
        except Exception as e:
            current_app.logger.error(e)

        self.number = None
        self.status = "stopped"
        self.message = None

        self.save()
        return self.to_dict()

    def remove_instance_folder_if_necessary(self):
        try:
            rmtree(self.instance_directory)
        except OSError as e:
            if not current_app.config["TESTING"]:
                current_app.logger.warning(e)

    def destroy(self):
        pass

    def timeout(self):
        self.stop()
        self.message = "Your instance has been stopped because it has expired."
        self.save()
        return self.to_dict()

    def extend_time(self):
        if self.stopped:
            return {"error": "Instance is stopped"}

        # If the expiration is in more than 1 hour the expiration time cannot be extended
        if (self.expiration - timedelta(seconds=3600)) > datetime.now():
            return False

        self.expiration += timedelta(seconds=3598)
        self.save()
        return self.to_dict()

    @property
    def started(self):
        return self.status == "started"

    @property
    def stopped(self):
        return self.status == "stopped"

    @property
    def instance_directory(self):
        return os.path.join(current_app.config["BASE_INSTANCE_DATA"], str(self.number))

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "message": self.message,
            "expiration": self.expiration.strftime("%m/%d/%Y, %H:%M:%S")
            if self.expiration
            else None,
            "challenge": self.resource.challenge.id,
            "server_time": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        }

    def fail_with_message(self, message):
        self.stop()
        self.status = "error"
        self.message = message
        self.delete()
        return self.to_dict()

    def get_new_instance_number(self):
        i = current_app.config["MIN_VM_INSTANCE_ID"]
        while os.path.exists(os.path.join(current_app.config["BASE_INSTANCE_DATA"], str(i))):
            if i >= current_app.config["MAX_VM_INSTANCE_ID"]:
                return -1
            i += 1
        return i


class TerraformInstance(ResourceInstance):
    __mapper_args__ = {"polymorphic_identity": "terraform"}

    def provide(self):
        try:
            if self.number:
                terraform_client = TerraformClient(instance_id=int(self.number))
                terraform_client.plan()
                terraform_client.apply()
                return terraform_client.output
            return None
        except CalledProcessError as e:
            current_app.logger.error(e, e.stderr)
            self.stop()
            return None
        except TerraformError as e:
            current_app.logger.error(e)
            return None

    def destroy(self):
        try:
            if self.number:
                terraform_client = TerraformClient(int(self.number))
                terraform_client.destroy()
                self.clean_resources_on_provider()
            return None
        except CalledProcessError as e:
            current_app.logger.error("in destroy", e, e.stderr)
        except TerraformError as e:
            current_app.logger.error(e)

    def clean_resources_on_provider(self):
        # deleteAllClones(int(self.number))
        pass


# No logic is required for FileInstance, as nothing is run. The file is only
# downloaded.
class FileInstance(ResourceInstance):
    __mapper_args__ = {"polymorphic_identity": "file"}
