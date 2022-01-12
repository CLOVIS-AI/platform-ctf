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

from ...tests.utils import DBTestCase
from ...models import ChallengeStep


class TestChallengeStep(DBTestCase):
    def test_challenge_step_creation(self):
        step = ChallengeStep(
            description="Un challenge",
            points=10,
            validation_type="string",
            validation_arg="flag{test}",
        )
        self.assertEqual(step.description, "Un challenge")
        self.assertEqual(step.points, 10)
        self.assertEqual(step.validation_type, "string")
        self.assertEqual(step.validation_arg, "flag{test}")
