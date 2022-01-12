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
from ..models import Documentation
from .command_utils import safe_open_file, save_new_model, test_model_before_delete

documentation_cli = AppGroup("documentation")


# region Commands related to import


@documentation_cli.command("import")
@click.option("-a", "--all", "_all", is_flag=True)
@click.option("-d", "--documentation", "short_name")
@click.option("-f", "--force", is_flag=True)
def import_documentation_command(_all, short_name, force):
    if _all:
        import_all_documentation(force_reimport=force)
    elif short_name:
        import_documentation(short_name, force_reimport=force)


def import_all_documentation(force_reimport=False):
    """Imports all the documentation present in the documentation folder and absent from the database."""
    for documentation_short_name in listdir(current_app.config["DOCUMENTATION_DIR"]):
        try:
            import_documentation(documentation_short_name, force_reimport=force_reimport)
        except(Exception,):
            pass


def import_documentation(documentation_short_name, force_reimport=False):
    """Imports the documentation named `short_name` into the database."""
    documentation_yaml_file = join(
        current_app.config["DOCUMENTATION_DIR"], documentation_short_name)

    if not isfile(documentation_yaml_file):
        print(f'File "{documentation_yaml_file}" not found.')
        return

    already_imported = (
        Documentation.query
        .filter(Documentation.short_name + ".yaml" == documentation_short_name)
        .one_or_none()
    )

    if already_imported:
        if force_reimport:
            reload_documentation_from_dir(documentation_short_name, already_imported)
        else:
            print(f"Documentation {documentation_short_name:40s} : already imported")
    else:
        load_documentation_from_dir(documentation_short_name)


def load_documentation_from_dir(documentation_short_name):
    try:
        data = load_documentation_yaml_from_dir(documentation_short_name)
        documentation = load_documentation_from_dict(data)
        documentation.save()
        print(f"Documentation {documentation_short_name:40s} : imported")
    except Exception as e:
        print(f"Documentation {documentation_short_name:40s} : {e}")


def load_documentation_from_dict(data):
    if "documentation" in data:
        return Documentation(**data["documentation"]).save()
    raise FileNotFoundError("No `documentation` key in yaml file.")


def reload_documentation_from_dir(documentation_short_name, documentation):
    data = load_documentation_yaml_from_dir(documentation_short_name)

    documentation.update(**data["documentation"])
    print(f"Documentation {documentation_short_name:40s} : reimported")


def load_documentation_yaml_from_dir(documentation):
    description_file = join(
        current_app.config["DOCUMENTATION_DIR"], documentation)
    try:
        return safe_open_file(description_file)
    except Exception as e:
        raise Exception(e)


# endregion
# region List of documentations


@documentation_cli.command("list")
def list_documentation_command():
    for documentation in Documentation.query:
        print(f"- {documentation.short_name}")

# endregion
# region Create documentation


@documentation_cli.command("create")
@click.option("-n", "--number", default=1)
def create_documentation_command(number):
    """Create `n` random documentation."""
    for _ in range(number):
        create_random_documentation()
    print(f"Created {number} documentation.")


def create_random_documentation():
    CATEGORIES = ["Reverse", "Crypto", "Web", "Pwn", "Forensic"]

    new_documentation = Documentation(
        name="Random doc {}",
        short_name="random_doc_{}",
        description="Cette documentation est une documentation généré aléatoirement.\n",
        category=choice(CATEGORIES),
    )

    # Using the documentation id to uniquify the documentation name and short_name
    save_new_model(new_documentation)

# endregion
# region Deletion


@documentation_cli.command("delete")
@click.option("-a", "--all", "_all", is_flag=True)
@click.option("-d", "--documentation", "short_name")
def delete_documentation_command(_all, short_name):
    if _all:
        delete_all_documentation()
    elif short_name:
        documentation = test_model_before_delete("Documentation", short_name, Documentation)
        if documentation:
            delete_documentation(documentation)


def delete_all_documentation():
    for documentation in Documentation.query:
        delete_documentation(documentation)


def delete_documentation(documentation):
    documentation.delete()
    print(f"Documentation {documentation.short_name:40s} : deleted")

# endregion
