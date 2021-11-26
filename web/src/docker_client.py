from docker import DockerClient

from .config import Config

config = Config()
client = DockerClient(base_url=f"ssh://{config.DOCKER_USER}@{config.DOCKER_HOSTNAME}:{config.DOCKER_PORT}")


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
