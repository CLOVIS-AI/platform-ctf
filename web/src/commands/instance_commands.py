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

from datetime import datetime

import click
from flask.cli import AppGroup

from ..config import Config
from ..docker_client import stop_container, get_all_running_container_ids
from ..models import ResourceInstance
from ..vcenter_client import getAllRunning, deleteAllClones

instance_cli = AppGroup("instance")

config = Config()


# region List instances

@instance_cli.command("list")
def list_instances_command():
    format_string = "{:^4} | {:^10s} | {:^16s} | {:^16s}"

    print(format_string.format("ID", "STATUS", "USERNAME", "CHALLENGE"))
    print("-" * len(format_string.format("", "", "", "")))

    for instance in ResourceInstance.query.all():
        print(
            format_string.format(
                str(instance.number) or "None",
                instance.status or "None",
                instance.user.username or "None",
                str(instance.resource.challenge.short_name) or "None",
            )
        )


# endregion
# region Check

@instance_cli.command("check")
@click.option("-i", "--inconsistency", is_flag=True)
@click.option("-e", "--expired", is_flag=True)
def check_instances_command(inconsistency, expired):
    if expired:
        check_expired_instances()
    if inconsistency:
        check_inconsistent_instances()


def check_expired_instances():
    """ This function checks for the presence of expired """
    print("\n> Checking for expired VMs\n")
    format_string = "{:^4} | {:^10s} | {:^16s} | {:^16s}"
    print(format_string.format("ID", "STATUS", "USERNAME", "CHALLENGE"))
    print("-" * len(format_string.format("", "", "", "")))

    expired = get_expired_instances()
    for i in expired:
        print(
            format_string.format(
                str(i.number) or "None",
                i.status or "None",
                i.user.username or "None",
                str(i.resource.challenge.short_name) or "None",
            )
        )

    print(f"\n{len(expired)} instance(s) have expired\n")


def check_inconsistent_instances():
    """ This function prints the inconsistencies found on the platform.
        It does not return anything. """
    print("\n> Checking for inconsistencies within platform\n")
    format_string = "{:^4} | {:^10s}"
    print(format_string.format("ID", "SOURCE", "USERNAME", "CHALLENGE"))
    print("-" * len(format_string.format("", "")))

    count_db = 0
    count_inst = 0
    inconsistencies = get_inconsistencies()
    for inst in inconsistencies["not_running"]:
        print(
            format_string.format(
                str(inst) or "None",
                "Database"
            )
        )
        count_db += 1
    for inst in inconsistencies["not_in_db"]["docker"]:
        print(
            format_string.format(
                str(inst) or None,
                "Docker"
            )
        )
        count_inst += 1
    for inst in inconsistencies["not_in_db"]["vm"]:
        print(
            format_string.format(
                str(inst),
                "VM"
            )
        )
        count_inst += 1
    print()
    if count_db > 0:
        print("WARNING : Some instances have been found in database but not running anywhere!")
    if count_inst > 0:
        print("BIGGER WARNING: Some instances are running but not present in database!")
        print("Some instances are running without a corresponding database record.")
        print("User could be unable to run another challenge corresponding to the running instance.")
        print("To clear this inconsistency, please consider running `flask instance clean -i`.")

    print(f"\n=> {count_db + count_inst} inconsistencies found.\n")


# endregion
# region Clean

@instance_cli.command("clean")
@click.option("-i", "--inconsistency", is_flag=True)
@click.option("-e", "--expired", is_flag=True)
def clean_instances_command(inconsistency, expired):
    if expired:
        clean_expired_instances()
    if inconsistency:
        clean_inconsistent_instances()


def clean_expired_instances():
    print("\n> Cleaning expired VMs")
    print("====================\n")
    expired = get_expired_instances()
    count = len(expired)
    errors = 0
    if count == 0:
        print("No expired instance found.\n")
        return

    print(f"{count} expired instance(s) found !\n")
    for instance in expired:
        try:
            stopping = instance.number
            print(f"Stopping {stopping}… ", end='')
            instance.stop()
            instance.message = "Your instance has been stopped because it has expired."
            instance.save()
            print(f"Instance stopped for user {instance.user.username}")
            count += 1
        except (Exception,):
            print(f"Failed to stop expired VM for user {instance.user.username}")

    if count > 1:
        print(f"{count} expired instances have been stopped\n")
    elif count == 1:
        print(f"{count} expired instance has been stopped\n")
    else:
        print("No expired instance has been stopped\n")

    if errors > 0:
        print("Errors have occurred…\n")


def clean_inconsistent_instances():
    """ Clean inconsistency between the database and providers (Docker, ESXI) """
    print("\n> Cleaning inconsistencies")
    print("====================\n")
    inconsistencies = get_inconsistencies()
    count = 0

    print("* stopping containers not in database…")
    for inst in inconsistencies["not_in_db"]["docker"]:
        print(f"- cleaning {inst}…")
        try:
            stop_container(inst)
            print(f"Successfully killed {inst}")
            count += 1
        except (Exception,):
            print(f"An error occurred while cleaning {inst}…")
    print(f"* killed {count} docker containers.\n")

    count = 0
    print("* Stopping VMs not in database…")
    for inst in inconsistencies["not_in_db"]["vm"]:
        print(f"- cleaning {inst}…")
        try:
            deleteAllClones(inst)
            print(f"Successfully killed {inst}")
        except (Exception,):
            print(f"An error occurred while cleaning {inst}…")
    print(f"* killed {count} VM instances.\n")

    count = 0
    print("* Cleaning database…")
    for entry in inconsistencies["not_running"]:
        print(f"- cleaning {entry}…")
        try:
            db_record = ResourceInstance.query.filter(ResourceInstance.number == entry).all()
            db_record.stop()
            db_record.message = "This entry has been removed due to an inconsistency"
            db_record.save()
            print(f"Successfully cleaned {entry}")
            count += 1
        except (Exception,):
            print(f"An error occurred while cleaning {entry}...")
    print(f"* cleaned {count} entries in database.\n")


# endregion
# region Internal functions

def get_expired_instances():
    expired = list()
    running_instances = ResourceInstance.query.filter(
        ResourceInstance.status != "stopped"
    ).all()

    for instance in running_instances:
        if instance.expiration <= datetime.now():
            expired.append(instance)

    return expired


def get_inconsistencies():
    """ This function returns a tuple of lists
        The first one is for the running containers not present in database
        The second one is for databases entries not linked to a running container """

    inconsistencies = {
        "not_in_db": {
            "docker": [],
            "vm": []
        },
        "not_running": []
    }

    db_running = ResourceInstance.query.filter(
        ResourceInstance.status != "stopped"
    ).all()
    docker_running = get_all_running_container_ids()
    vm_running = getAllRunning()

    for vm_instance in vm_running:
        if config.MIN_VM_INSTANCE_ID <= vm_instance <= config.MAX_VM_INSTANCE_ID:
            if vm_instance not in db_running:
                print(f"Inconsistency found! {vm_instance}")
                inconsistencies["not_in_db"]["vm"].append(vm_instance)

    for docker_instance in docker_running:
        if config.MIN_VM_INSTANCE_ID <= docker_instance <= config.MAX_VM_INSTANCE_ID:
            if docker_running not in db_running:
                print(f"Inconsistency found! {docker_instance}")
                inconsistencies["not_in_db"]["docker"].append(docker_instance)

    for running in db_running:
        found = False
        if config.MIN_VM_INSTANCE_ID <= running.number <= config.MAX_VM_INSTANCE_ID:
            if running in docker_running:
                found = True
            if running in vm_running:
                found = True
        if not found:
            inconsistencies["not_running"].append(running.number)

    return inconsistencies

# endregion
