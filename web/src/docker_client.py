import sys

from docker import DockerClient

from .config import Config

config = Config()

try:
    client = DockerClient(base_url=f"ssh://{config.DOCKER_USER}@{config.DOCKER_HOSTNAME}:{config.DOCKER_PORT}")

    # region The Docker client is properly configured

    def _isContainerRunning(instance_id):
        """
        Checks if there is a running container for this instance id
        """
        running = client.containers.list()
        for inst in running:
            if int(inst.name.split("_")[1]) == instance_id:
                return True
        return False

    def _getContainer(instance_id):
        """
        Gets a docker container object from an instance id
        """
        if not _isContainerRunning(instance_id):
            print(f"It appears that {instance_id} is not a running container.")
            return 1
        running = client.containers.list()
        for inst in running:
            if int(inst.name.split("_")[1]) == instance_id:
                return inst

    def stopContainer(instance_id):
        """
        Stops a running container.
        If the instance_id is incorrect, raises an error.
        """
        if not _isContainerRunning(instance_id):
            print(f"It appears that {instance_id} is not a running container.")
            return 1
        to_stop = _getContainer(instance_id)
        try:
            to_stop.stop()
            to_stop.remove()
        except (Exception,):
            print(
                f"An error occurred while trying to kill container for instance {instance_id}!"
            )
            return 1
        return 0

    def getAllRunningContainersIds():
        """
        Returns all the instance ids of running docker containers
        """
        running = client.containers.list()
        inst_ids = list()
        for inst in running:
            inst_ids.append(int(inst.name.split("_")[1]))

        return inst_ids

    # endregion
except OSError:
    # region The docker client is not configured, implement all actions as NO-OPs
    print("The docker client has not been configured. This server will not attempt to connect to it.", file=sys.stderr)

    def _isContainerRunning(_):
        print("NOOP in docker_client.py:_isContainerRunning, because the Docker client is not configured.",
              file=sys.stderr)
        return False  # no container is running

    def _getContainer(_):
        print("NOOP in docker_client.py:_getContainer, because the Docker client is not configured.", file=sys.stderr)
        return 1  # same error code as the normal function if the container isn't running

    def stopContainer(_):
        print("NOOP in docker_client.py:stopContainer, because the Docker client is not configured.", file=sys.stderr)
        return 1  # same error code as the normal function if the container isn't running

    def getAllRunningContainersIds():
        print("NOOP in docker_client.py:getAllRunningContainersIds, because the Docker client is not configured.",
              file=sys.stderr)
        return []  # no containers can be running

    # endregion
