#  CTF Platform by RSR, educational platform to try cyber-security challenges
#  Copyright (C) 2022 ENSEIRB-MATMECA, Bordeaux-INP, RSR formation since 2018
#  Supervised by Toufik Ahmed, tad@labri.fr
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

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
