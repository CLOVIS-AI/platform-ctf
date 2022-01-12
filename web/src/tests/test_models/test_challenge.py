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
from ...models import Challenge


class TestChallenge(DBTestCase):
    def test_challenge_creation(self):
        challenge = Challenge(
            name="Long name", short_name="short_name", description="description"
        )
        self.assertEqual(challenge.name, "Long name")
        self.assertEqual(challenge.short_name, "short_name")
        self.assertEqual(challenge.description, "description")

    def test_cannot_create_empty_challenge(self):
        with self.assertRaises(Exception):
            Challenge().save()
        with self.assertRaises(Exception):
            Challenge(name="Challenge number one").save()
        with self.assertRaises(Exception):
            Challenge(short_name="chall").save()

    def test_short_name_are_unique(self):
        Challenge(name="Challenge number one", short_name="chall").save()
        with self.assertRaises(Exception):
            Challenge(name="Challenge number two", short_name="chall").save()
