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

from flask.helpers import url_for
from flask_login import current_user

from .utils import PopulatedDBTestCase
from ..commands import challenge_cli
from ..models import User
from ..models.challenge_validation import ChallengeValidation


# noinspection DuplicatedCode
class TestRoutes(PopulatedDBTestCase):
    def login(self, username, password):
        return self.client.post(
            "/login",
            data=dict(username=username, password=password),
            follow_redirects=True,
        )

    def logout(self):
        return self.client.get("/logout", follow_redirects=True)

    def test_index_page_is_accessible(self):
        response = self.client.get("/")
        self.assertTemplateUsed("index.jinja2")
        self.assert200(response)

        response = self.client.get("/index")
        self.assertTemplateUsed("index.jinja2")
        self.assert200(response)

    def test_challenges_page_is_accessible_with_challenges(self):
        self.runner = self.app.test_cli_runner()
        self.runner.invoke(challenge_cli, ["import", "-c", "valid_challenge"])
        self.runner.invoke(challenge_cli, ["import", "-c", "valid_challenge_2"])

        response = self.client.get("/challenges")
        self.assertTemplateUsed("challenges.jinja2")

        self.assert200(response)

    def test_challenges_page_when_connected(self):
        with self.client:
            self.login("logged_user", "logged_password")
            response = self.client.get("/challenges")
            self.assertTemplateUsed("challenges.jinja2")
            self.assert200(response)

    def test_scenarios_page_when_connected(self):
        with self.client:
            self.login("logged_user", "logged_password")
            response = self.client.get("/scenarios")
            self.assertTemplateUsed("scenarios_trainings.jinja2")
            self.assert200(response)

    def test_trainings_page_when_connected(self):
        with self.client:
            self.login("logged_user", "logged_password")
            response = self.client.get("/trainings")
            self.assertTemplateUsed("scenarios_trainings.jinja2")
            self.assert200(response)

    def test_individual_challenge_page_is_accessible(self):
        response = self.client.get("/challenge/1")
        self.assertTemplateUsed("challenge.jinja2")
        self.assert200(response)

    def test_individual_challenge_page_does_not_exist(self):
        response = self.client.get("/challenge/404")
        self.assert404(response)

    def test_individual_challenge_page_when_connected(self):
        with self.client:
            self.login("logged_user", "logged_password")
            response = self.client.get("/challenge/1")
            self.assertTemplateUsed("challenge.jinja2")
            self.assert200(response)

    def test_inexistant_challenge_page_is_inaccessible(self):
        response = self.client.get("/challenge/100")
        self.assert404(response)
        self.assertTemplateUsed("404.jinja2")

    def test_unauthenticated_action_on_challenge(self):
        response = self.client.post("/challenge/1")
        self.assert403(response)

    def test_user_login_succeed(self):
        with self.client:
            response = self.login("logged_user", "logged_password")
            self.assert200(response)
            self.assertTrue(current_user.is_authenticated)

    def test_user_logout(self):
        with self.client:
            self.login("logged_user", "logged_password")
            response = self.logout()
            self.assert200(response)

    def test_user_login_with_wrong_password_fail(self):
        response = self.login("logged_user", "wrong_password")
        self.assert200(response)
        self.assertIn(b"Invalid username or password", response.data)

    def test_user_login_with_unknown_username_fail(self):
        response = self.login("unknown_user", "random_password")
        self.assert200(response)
        self.assertIn(b"Invalid username or password", response.data)

    def test_action_on_nonexistent_challenge(self):
        self.login("logged_user", "logged_password")
        response = self.client.post("/challenge/100")
        self.assert404(response)

    def test_ranking(self):
        response = self.client.get(url_for("main.ranking"))
        self.assert200(response)
        print(response.data.decode())

        # A player with points is present
        self.assertIn("user1", response.data.decode())
        self.assertIn("30", response.data.decode())

        # A player without points is absent
        self.assertFalse("user_admin" in response.data.decode())

    def test_reset_progress(self):
        # Login is required
        response = self.client.post(url_for("main.settings"), data={
            "username": "logged_user", "pr_reset_submit": "Reset+all+my+progress"
        })
        self.assertRedirects(response, url_for(
            "main.login", next=(url_for("main.settings"))))

        with self.client:
            self.login("logged_user", "logged_password")

            # The user has some progress
            validations = ChallengeValidation.query.filter(ChallengeValidation.user == current_user).all()
            self.assertFalse(validations == [])

            # The user reset its progress
            self.client.post(url_for("main.settings"), data={
                "username": "logged_user", "pr_reset_submit": "Reset+all+my+progress"})

            # The user has no progress
            validations = ChallengeValidation.query.filter(
                ChallengeValidation.user == current_user).all()
            self.assertTrue(validations == [])

            # Other user has some progress
            other_user = User.query.filter(User.username == "user1").one()
            validations = ChallengeValidation.query.filter(
                ChallengeValidation.user == other_user).all()
            self.assertFalse(validations == [])

            # The user reset other user's progress
            self.client.post(url_for("main.settings"), data={
                "username": "user1", "pr_reset_submit": "Reset+all+my+progress"})

            # Other user still has progress
            validations = ChallengeValidation.query.filter(
                ChallengeValidation.user == other_user).all()
            self.assertFalse(validations == [])
