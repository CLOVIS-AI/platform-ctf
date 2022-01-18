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

import click

from os.path import join, isfile
from os import listdir
from random import choice
from flask.cli import AppGroup
from flask import current_app
from ..models import Help
from .command_utils import safe_open_file, save_new_model, test_model_before_delete

help_cli = AppGroup("help")


# region Commands related to import


@help_cli.command("import")
@click.option("-a", "--all", "_all", is_flag=True)
@click.option("-d", "--help", "short_name")
@click.option("-f", "--force", is_flag=True)
def import_help_command(_all, short_name, force):
    if _all:
        import_all_help(force_reimport=force)
    elif short_name:
        import_help(short_name, force_reimport=force)


def import_all_help(force_reimport=False):
    """Imports all the help present in the help folder and absent from the database."""
    for help_short_name in listdir(current_app.config["HELP_DIR"]):
        try:
            import_help(help_short_name, force_reimport=force_reimport)
        except(Exception,):
            pass


def import_help(help_short_name, force_reimport=False):
    """Imports the help named `short_name` into the database."""
    help_yaml_file = join(
        current_app.config["HELP_DIR"], help_short_name)

    if not isfile(help_yaml_file):
        print(f'File "{help_yaml_file}" not found.')
        return

    already_imported = (
        Help.query
        .filter(Help.short_name + ".yaml" == help_short_name)
        .one_or_none()
    )

    if already_imported:
        if force_reimport:
            reload_help_from_dir(help_short_name, already_imported)
        else:
            print(f"Help {help_short_name:40s} : already imported")
    else:
        load_help_from_dir(help_short_name)


def load_help_from_dir(help_short_name):
    try:
        data = load_help_yaml_from_dir(help_short_name)
        help = load_help_from_dict(data)
        help.save()
        print(f"Help {help_short_name:40s} : imported")
    except Exception as e:
        print(f"Help {help_short_name:40s} : {e}")


def load_help_from_dict(data):
    if "help" in data:
        return Help(**data["help"]).save()
    raise FileNotFoundError("No `help` key in yaml file.")


def reload_help_from_dir(help_short_name, help):
    data = load_help_yaml_from_dir(help_short_name)

    help.update(**data["help"])
    print(f"Help {help_short_name:40s} : reimported")


def load_help_yaml_from_dir(help):
    description_file = join(
        current_app.config["HELP_DIR"], help)
    try:
        return safe_open_file(description_file)
    except Exception as e:
        raise Exception(e)


# endregion
# region List of helps


@help_cli.command("list")
def list_help_command():
    for help in Help.query:
        print(f"- {help.short_name}")

# endregion
# region Create help


@help_cli.command("create")
@click.option("-n", "--number", default=1)
def create_help_command(number):
    """Create `n` random help."""
    for _ in range(number):
        create_random_help()
    print(f"Created {number} help.")


def create_random_help():
    CATEGORIES = ["Reverse", "Crypto", "Web", "Pwn", "Forensic"]

    new_help = Help(
        name="Random doc {}",
        short_name="random_doc_{}",
        description="Cette help est une help généré aléatoirement.\n",
        category=choice(CATEGORIES),
    )

    # Using the help id to uniquify the help name and short_name
    save_new_model(new_help)

# endregion
# region Deletion


@help_cli.command("delete")
@click.option("-a", "--all", "_all", is_flag=True)
@click.option("-d", "--help", "short_name")
def delete_help_command(_all, short_name):
    if _all:
        delete_all_help()
    elif short_name:
        help = test_model_before_delete("Help", short_name, Help)
        if help:
            delete_help(help)


def delete_all_help():
    for help in Help.query:
        delete_help(help)


def delete_help(help):
    help.delete()
    print(f"Help {help.short_name:40s} : deleted")

# endregion
