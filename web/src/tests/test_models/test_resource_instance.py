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
from ...models import ResourceInstance, Challenge, ChallengeResource, User


# noinspection DuplicatedCode
class TestResourceInstance(DBTestCase):
    def test_resource_instance_creation(self):
        user = User(username="username", email="email@email.com").save()
        Challenge(name="Long name", short_name="short_name").save()
        challenge_resource = ChallengeResource(type="file", args="filename.txt").save()
        resource_instance = ResourceInstance(
            resource=challenge_resource, user=user
        ).save()
        self.assertEqual(resource_instance.user, user)
        self.assertEqual(resource_instance.resource, challenge_resource)

    def test_resource_instance_instantiation(self):
        user = User(username="username", email="email@email.com").save()
        challenge_resource = ChallengeResource(type="terraform", args="test").save()
        challenge_resource.instantiate(user)
