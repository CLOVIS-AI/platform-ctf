from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey, Column
from sqlalchemy.types import Integer, String, Boolean

from .resource_instance import ResourceInstance
from ..extensions import db


class ChallengeResource(db.Model):
    """
    A physical resource that can be started by users.

    The Resource class represents the resource itself, whereas the Instance class represents the usage of a
    resource by a user.

    Currently, there are two types of resources:
    - Virtual machines,
    - Docker containers.
    """

    id = Column(Integer, primary_key=True)
    type = Column(String(64))
    args = Column(String(64), default="")
    start_duration = Column(Integer, default=0)
    is_vpn_needed = Column(Boolean, default=False)
    challenge_id = Column(Integer, ForeignKey("challenge.id"))

    instances = relationship("ResourceInstance", back_populates="resource")
    challenge = relationship("Challenge", back_populates="resource")

    __mapper_args__ = {"polymorphic_identity": "resource", "polymorphic_on": type}

    def instantiate(self, user):
        if user.instance:
            user.instance.stop()
            user.instance.delete()
        return ResourceInstance(type=self.type, user=user, resource=self).save()


class TerraformResource(ChallengeResource):
    __mapper_args__ = {"polymorphic_identity": "terraform"}


class FileResource(ChallengeResource):
    __mapper_args__ = {"polymorphic_identity": "file"}
