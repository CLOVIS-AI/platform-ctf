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
from ...models import User


# noinspection DuplicatedCode
class TestUser(DBTestCase):
    def test_user_creation(self):
        user = User(username="username", email="email")
        assert user.username == "username"
        assert user.email == "email"

    def test_cannot_create_empty_user(self):
        with self.assertRaises(Exception):
            User().save()
            User(username="test_user").save()
            User(email="test_user@email.com").save()

    def test_cannot_create_user_with_same_username(self):
        User(username="test_user", email="test_user@email.com").save()
        with self.assertRaises(Exception):
            User(username="test_user", email="test_user2@email.com").save()

    def test_cannot_create_user_with_same_email(self):
        User(username="test_user", email="test_user@email.com").save()
        with self.assertRaises(Exception):
            User(username="test_user2", email="test_user@email.com").save()

    def test_user_password_is_hashed(self):
        user = User(username="username", email="email")
        user.set_password("test_password".encode())
        assert user.password != "test_password"

    def test_user_check_password(self):
        user = User(username="username", email="email")
        user.set_password("test_password".encode())
        assert user.check_password("test_password")
        assert not user.check_password("wrong_password")

    def test_banned_user_cannot_access_logged_content(self):
        user = User(username="username", email="email", is_banned=True)
        assert not user.can_access_logged_content()
