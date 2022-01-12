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

from .utils import PopulatedDBTestCase


# noinspection DuplicatedCode
class TestRoutesAdmin(PopulatedDBTestCase):
    def login(self, username, password):
        return self.client.post(
            "/login",
            data=dict(username=username, password=password),
            follow_redirects=True,
        )

    def logout(self):
        return self.client.get("/logout", follow_redirects=True)

    def test_admin_page_is_inaccessible_when_not_connected(self):
        response = self.client.get("/admin")
        self.assertRedirects(response, "/login?next=%2Fadmin")

    def test_admin_page_is_inaccessible_when_not_admin(self):
        with self.client:
            self.login("logged_user", "logged_password")
            response = self.client.get("/admin")
            self.assert403(response)

    def test_admin_challenge_page_is_inaccessible_when_not_connected(self):
        response = self.client.get("/admin/challenges")
        self.assertRedirects(response, "/login?next=%2Fadmin%2Fchallenges")

    def test_admin_challenge_page_is_inaccessible_when_not_admin(self):
        with self.client:
            self.login("logged_user", "logged_password")
            response = self.client.get("/admin/challenges")
            self.assert403(response)

    def test_admin_user_page_is_inaccessible_when_not_connected(self):
        response = self.client.get("/admin/users")
        self.assertRedirects(response, "/login?next=%2Fadmin%2Fusers")

    def test_admin_user_page_is_inaccessible_when_not_admin(self):
        with self.client:
            self.login("logged_user", "logged_password")
            response = self.client.get("/admin/users")
            self.assert403(response)

    def test_admin_instances_page_is_inaccessible_when_not_connected(self):
        response = self.client.get("/admin/instances")
        self.assertRedirects(response, "/login?next=%2Fadmin%2Finstances")

    def test_admin_instances_page_is_inaccessible_when_not_admin(self):
        with self.client:
            self.login("logged_user", "logged_password")
            response = self.client.get("/admin/instances")
            self.assert403(response)
