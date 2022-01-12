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

from ...commands import user_cli
from ...models import User, ChallengeStep
from ...tests.utils import CliTestCase


# noinspection DuplicatedCode
class TestUsersCommands(CliTestCase):

    def test_list(self):
        User(username="u1", email="u1@u.com").save()
        User(username="u2", email="u2@u.com").save()
        User(username="u3", email="u3@u.com").save()
        User(username="u4", email="u4@u.com").save()
        User(username="u5", email="u5@u.com").save()
        result = self.runner.invoke(user_cli, ["list"])

        self.assertEqual(result.exit_code, 0, msg=result.exception)
        self.assertIn("u1", result.stdout)
        self.assertIn("u1@u.com", result.stdout)
        self.assertIn("u5", result.stdout)

    def test_create_without_arg(self):
        result = self.runner.invoke(user_cli, ["create"])
        self.assertEqual(result.exit_code, 0, msg=result.exception)
        self.assertEqual(
            result.stdout,
            "No challenge created, use --random or --username and --email\n",
        )
        self.assertEqual(User.query.count(), 0)

    def test_create_one_random_user(self):
        result = self.runner.invoke(
            user_cli, ["create", "--random", "-n", "1"])
        self.assertEqual(result.exit_code, 0, msg=result.exception)
        self.assertEqual(result.stdout, "Created 1 random users.\n")
        self.assertEqual(User.query.count(), 1)

    def test_create_many_random_users(self):
        # Create ChallengeStep that can be used by the random generator
        ChallengeStep(description="What is the flag ?").save()
        ChallengeStep(description="What is the flag ?").save()
        ChallengeStep(description="What is the flag ?").save()
        ChallengeStep(description="What is the flag ?").save()

        result = self.runner.invoke(
            user_cli, ["create", "--random", "-n", "10"])
        self.assertEqual(result.exit_code, 0, msg=result.exception)
        self.assertEqual(result.stdout, "Created 10 random users.\n")
        self.assertEqual(User.query.count(), 10)

    def test_create_user_with_args(self):
        result = self.runner.invoke(
            user_cli,
            [
                "create",
                "--username",
                "username",
                "--email",
                "username@email.com",
                "--password",
                "password",
            ],
        )
        self.assertEqual(result.exit_code, 0, msg=result.exception)
        self.assertEqual(result.stdout, "")
        users = User.query.all()
        self.assertEqual(len(users), 1)
        user = users[0]
        self.assertEqual(user.username, "username")
        self.assertEqual(user.email, "username@email.com")
        self.assertNotEqual(user.password, "password")

    def test_create_user_with_already_used_username(self):
        self.runner.invoke(
            user_cli,
            [
                "create",
                "--username",
                "username",
                "--email",
                "username@email.com",
                "--password",
                "password",
            ],
        )
        result = self.runner.invoke(
            user_cli,
            [
                "create",
                "--username",
                "username",
                "--email",
                "username1@email.com",
                "--password",
                "password",
            ],
        )
        self.assertEqual(result.exit_code, 0, msg=result.exception)
        self.assertEqual(
            result.stdout, "User {:16.16s} : username already used\n".format(
                "username")
        )

    def test_create_user_with_already_used_email(self):
        self.runner.invoke(
            user_cli,
            [
                "create",
                "--username",
                "username",
                "--email",
                "username@email.com",
                "--password",
                "password",
            ],
        )
        result = self.runner.invoke(
            user_cli,
            [
                "create",
                "--username",
                "username2",
                "--email",
                "username@email.com",
                "--password",
                "password",
            ],
        )
        self.assertEqual(result.exit_code, 0, msg=result.exception)
        self.assertEqual(
            result.stdout, "User {:16.16s} : email already used\n".format(
                "username2")
        )

    def test_delete_without_args(self):
        result = self.runner.invoke(user_cli, ["delete"])
        self.assertEqual(
            result.stdout,
            "No user deleted, use --all or <user_id>\n",
            msg=result.exception,
        )

    def test_delete_one_user(self):
        user = User(username="username", email="username@email.com").save()
        result = self.runner.invoke(user_cli, ["delete", str(user.id)])
        self.assertEqual(result.exit_code, 0, msg=result.exception)
        self.assertEqual(
            result.stdout,
            "User {:16.16s} : deleted\n".format(user.username),
            msg=result.exception,
        )

    def test_delete_inexistant_user(self):
        result = self.runner.invoke(user_cli, ["delete", "1"])
        self.assertEqual(result.exit_code, 0, msg=result.exception)
        self.assertIn("does not exist", result.stdout)

    def test_delete_all_users(self):
        self.runner.invoke(user_cli, ["create", "--random", "-n", "10"])
        result = self.runner.invoke(user_cli, ["delete", "--all"])
        self.assertEqual(result.exit_code, 0, msg=result.exception)
        self.assertEqual(result.stdout.count(
            "deleted\n"), 10, msg=result.exception)
        self.assertEqual(User.query.count(), 0)

    def test_admin_without_command(self):
        result = self.runner.invoke(user_cli, ["admin", "1"])
        self.assertEqual(result.exit_code, 0, msg=result.exception)
        self.assertIn("Please chose an option", result.stdout)

    def test_admin_promote(self):
        u1 = User(username="u1", email="u1@u.com").save()
        User(username="u2", email="u2@u.com").save()
        self.assertFalse(u1.is_admin)

        result = self.runner.invoke(
            user_cli, ["admin", "--promote", str(u1.id)])
        self.assertEqual(result.exit_code, 0, msg=result.exception)
        self.assertIn("promoted", result.stdout)

        self.assertTrue(u1.is_admin)

    def test_admin_revoke(self):
        u1 = User(username="u1", email="u1@u.com", is_admin=True).save()
        User(username="u2", email="u2@u.com", is_admin=True).save()

        result = self.runner.invoke(
            user_cli, ["admin", "--revoke", str(u1.id)])
        self.assertEqual(result.exit_code, 0, msg=result.exception)
        self.assertIn("revoked", result.stdout)

        self.assertFalse(u1.is_admin)

    def test_admin_cannot_revoke_last_admin(self):
        u1 = User(username="u1", email="u1@u.com", is_admin=True).save()
        User(username="u2", email="u2@u.com").save()

        result = self.runner.invoke(
            user_cli, ["admin", "--revoke", str(u1.id)])
        self.assertEqual(result.exit_code, 0, msg=result.exception)
        self.assertIn(
            "Impossible to revoke the last administrator", result.stdout)

    def test_promote_nonexistent_user(self):
        result = self.runner.invoke(user_cli, ["admin", "--revoke", "1"])
        self.assertEqual(result.exit_code, 0, msg=result.exception)
        self.assertIn("does not exist", result.stdout)

    def test_promote_user_already_admin(self):
        u1 = User(username="u1", email="u1@u.com", is_admin=True).save()
        result = self.runner.invoke(user_cli, ["admin", "--promote", str(u1.id)])
        self.assertEqual(result.exit_code, 0, msg=result.exception)
        self.assertIn("Nothing to do", result.stdout)
