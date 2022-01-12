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
