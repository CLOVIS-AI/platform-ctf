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

import string
from random import choice, randrange

import click
from flask.cli import AppGroup

from ..models import User, ChallengeValidation, ChallengeStep

user_cli = AppGroup("user")


# region List of users

@user_cli.command("list")
def list_users_command():
    format_string = "{:^4.4s} | {:^16.16s} | {:^30.30} | {:^5.5s} | {:^6.6s}"

    print(format_string.format("ID", "USERNAME", "EMAIL", "ADMIN", "BANNED"))
    print("-" * len(format_string.format("", "", "", "", "", "")))

    for user in User.query:
        print(
            format_string.format(
                str(user.id) or "None",
                user.username or "None",
                user.email or "None",
                str(user.is_admin) or "None",
                str(user.is_banned) or "None",
            )
        )


# endregion
# region Create

@user_cli.command("create")
@click.option("--random", is_flag=True)
@click.option("-n", "--number", default=1)
@click.option("--admin", "is_admin", is_flag=True)
@click.option("-u", "--username")
@click.option("-m", "--email")
@click.option("-p", "--password")
def create_user_command(random, number, username, email, password, is_admin):
    """Create users."""
    if random:
        for _ in range(number):
            create_random_user()
        print(f"Created {number} random users.")
    elif username and email:
        create_user(username, email, password, is_admin)
    else:
        print("No challenge created, use --random or --username and --email")


def generate_random_password():
    return "".join([choice(string.ascii_letters) for _ in range(10)])


def create_random_user():
    new_user = create_user(
        "temporary_username_3",
        "temporary_email_3",
        password=generate_random_password(),
        is_admin=choice([True, False]),
    )
    new_user.username = "random_user_{}".format(new_user.id)
    new_user.email = "random_user_{}@mail.rsr".format(new_user.id)

    steps_number = ChallengeStep.query.count()
    if steps_number:
        for _ in range(randrange(1, steps_number)):
            add_random_validation_to_user(new_user)

    new_user.save()


def create_user(username, email, password=None, is_admin=False):
    if check_username_already_used(username):
        print(f"User {username:16.16s} : username already used")
        return

    if check_email_already_used(email):
        print(f"User {username:16.16s} : email already used")
        return

    # PyCharm doesn't understand why these arguments are given. I don't either.
    # noinspection PyArgumentList
    new_user = User(username=username, email=email, is_admin=is_admin).save()

    if not password:
        password = generate_random_password()
    new_user.set_password(password.encode())

    return new_user.save()


def add_random_validation_to_user(user):
    steps = ChallengeStep.query.all()
    ChallengeValidation(user_id=user.id, challenge_step_id=choice(steps).id)


def check_username_already_used(username):
    return User.query.filter(User.username == username).all()


def check_email_already_used(email):
    return User.query.filter(User.email == email).all()


# endregion
# region Delete

@user_cli.command("delete")
@click.option("-a", "--all", "_all", is_flag=True)
@click.argument("user_id", type=int, required=False)
def delete_user_command(_all, user_id):
    """Delete users."""
    if _all:
        for user in User.query:
            delete_user(user)
    elif user_id:
        user = User.query.filter(User.id == user_id).one_or_none()
        if not user:
            print(f"User {user_id} does not exist")
            return
        delete_user(user)
    else:
        print("No user deleted, use --all or <user_id>")


def delete_user(user):
    user.delete()
    print(f"User {user.username:16.16s} : deleted")


# endregion
# region Administration

@user_cli.command("admin")
@click.option("-p", "--promote", is_flag=True)
@click.option("-r", "--revoke", is_flag=True)
@click.argument("user_id", type=int, required=True)
def promote_revoke_admin(promote, revoke, user_id):
    """Promote or revoke an administrator."""

    if not promote and not revoke:
        print("Please chose an option between promote and revoke an administrator")
        return

    user = User.get(user_id)
    if not user:
        print(f"User {user_id} does not exist")
        return

    if revoke:
        if User.query.filter(User.is_admin).count() <= 1:
            print(
                "Impossible to revoke the last administrator. Please promote another admin before."
            )
            return

    if not user.is_admin and promote:
        user.is_admin = True
        user.save()
        print(f"{user.username} promoted to administrator")

    elif user.is_admin and revoke:
        user.is_admin = False
        user.save()
        print(f"{user.username} revoked from the administrators")

    else:
        print("Nothing to do")

# endregion
