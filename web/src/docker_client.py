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

import sys

from docker import DockerClient

from .config import Config

config = Config()

if config.DOCKER_USER != "" and config.DOCKER_HOSTNAME != "" and config.DOCKER_PORT != "":
    client = DockerClient(base_url=f"ssh://{config.DOCKER_USER}@{config.DOCKER_HOSTNAME}:{config.DOCKER_PORT}")

    # region The Docker client is properly configured

    def _is_container_running(instance_id):
        """
        Checks if there is a running container for this instance id
        """
        running = client.containers.list()
        for inst in running:
            if int(inst.name.split("_")[1]) == instance_id:
                return True
        return False

    def _get_container(instance_id):
        """
        Gets a docker container object from an instance id
        """
        if not _is_container_running(instance_id):
            print(f"It appears that {instance_id} is not a running container.")
            return 1
        running = client.containers.list()
        for inst in running:
            if int(inst.name.split("_")[1]) == instance_id:
                return inst

    def stop_container(instance_id):
        """
        Stops a running container.
        If the instance_id is incorrect, raises an error.
        """
        if not _is_container_running(instance_id):
            print(f"It appears that {instance_id} is not a running container.")
            return 1
        to_stop = _get_container(instance_id)
        try:
            to_stop.stop()
            to_stop.remove()
        except (Exception,):
            print(
                f"An error occurred while trying to kill container for instance {instance_id}!"
            )
            return 1
        return 0

    def get_all_running_container_ids():
        """
        Returns all the instance ids of running docker containers
        """
        running = client.containers.list()
        inst_ids = list()
        for inst in running:
            inst_ids.append(int(inst.name.split("_")[1]))

        return inst_ids

    # endregion
else:
    # region The docker client is not configured, implement all actions as NO-OPs
    print("The docker client has not been configured. This server will not attempt to connect to it.", file=sys.stderr)

    def _is_container_running(_):
        print("NOOP in docker_client.py:_isContainerRunning, because the Docker client is not configured.",
              file=sys.stderr)
        return False  # no container is running

    def _get_container(_):
        print("NOOP in docker_client.py:_getContainer, because the Docker client is not configured.", file=sys.stderr)
        return 1  # same error code as the normal function if the container isn't running

    def stop_container(_):
        print("NOOP in docker_client.py:stopContainer, because the Docker client is not configured.", file=sys.stderr)
        return 1  # same error code as the normal function if the container isn't running

    def get_all_running_container_ids():
        print("NOOP in docker_client.py:getAllRunningContainersIds, because the Docker client is not configured.",
              file=sys.stderr)
        return []  # no containers can be running

    # endregion
