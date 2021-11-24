import atexit
import re

from pyVim import connect
# PyCharm can't find the 'vmodl' and 'vim' symbols
# noinspection PyUnresolvedReferences
from pyVmomi import vmodl, vim

from .config import Config

config = Config()


# Helper function for task operations
def _wait_for_tasks(service_instance, tasks):
    """Given the service instance si and tasks, it returns after all the
    tasks are complete
    """
    property_collector = service_instance.content.propertyCollector
    task_list = [str(task) for task in tasks]
    # Create filter
    obj_specs = [vmodl.query.PropertyCollector.ObjectSpec(obj=task) for task in tasks]
    property_spec = vmodl.query.PropertyCollector.PropertySpec(
        type=vim.Task, pathSet=[], all=True
    )
    filter_spec = vmodl.query.PropertyCollector.FilterSpec()
    filter_spec.objectSet = obj_specs
    filter_spec.propSet = [property_spec]
    pcfilter = property_collector.CreateFilter(filter_spec, True)
    try:
        version, state = None, None
        # Loop looking for updates till the state moves to a completed state.
        while len(task_list):
            update = property_collector.WaitForUpdates(version)
            for filter_set in update.filterSet:
                for obj_set in filter_set.objectSet:
                    task = obj_set.obj
                    for change in obj_set.changeSet:
                        if change.name == "info":
                            state = change.val.state
                        elif change.name == "info.state":
                            state = change.val
                        else:
                            continue

                        if not str(task) in task_list:
                            continue

                        if state == vim.TaskInfo.State.success:
                            # Remove task from taskList
                            task_list.remove(str(task))
                        elif state == vim.TaskInfo.State.error:
                            raise task.info.error
            # Move to next version
            version = update.version
    finally:
        if pcfilter:
            pcfilter.Destroy()


def _getHost(si):
    content = si.RetrieveContent()

    container = content.rootFolder

    viewType = [vim.HostSystem]
    recursive = True

    children = content.viewManager.CreateContainerView(
        container, viewType, recursive
    ).view

    # There is only one host (for the moment), it is returned
    return children[0]


def _getAllVms(si):
    content = si.RetrieveContent()

    container = content.rootFolder

    viewType = [vim.VirtualMachine]
    recursive = True

    children = content.viewManager.CreateContainerView(
        container, viewType, recursive
    ).view

    # Returns all VMs that start with "clonevm_xx_" where xx is a number
    vms_to_return = []
    for vm in children:
        vmname = vm.summary.config.name
        if "vCenter" not in vmname and re.match("^clonevm_[0-9]+_*", vmname):
            vms_to_return.append(vm)

    return vms_to_return


def _getAllVSwitchs(si):
    host = _getHost(si)

    vswitchs = host.config.network.vswitch

    # Returns all vSwitches that start with "clonesw_xx_" where xx is a number
    vswitchs_to_return = []
    for vswitch in vswitchs:
        vswitchname = vswitch.name
        if "vCenter" not in vswitchname and re.match("^clonesw_[0-9]+_*", vswitchname):
            vswitchs_to_return.append(vswitch)

    return vswitchs_to_return


def _getAllPortsGroups(si):
    content = si.RetrieveContent()

    container = content.rootFolder

    viewType = [vim.Network]
    recursive = True

    children = content.viewManager.CreateContainerView(
        container, viewType, recursive
    ).view

    # Returns all PortsGroups that start with "clonesw_pg_" where xx is a number
    portsgroups_to_return = []
    for portsgroup in children:
        portsgroupname = portsgroup.name
        if "vCenter" not in portsgroupname and re.match(
                "^clonepg_[0-9]+_*", portsgroupname
        ):
            portsgroups_to_return.append(portsgroup)

    return portsgroups_to_return


# Returns a list of integers, which correspond to the identifiers of instances running on the vCenter
def getAllRunning():
    # Connection to the vCenter: creation of the service instance and registration with atexit (?)
    si = connect.SmartConnectNoSSL(
        host=config.VCENTER_HOST, user=config.VCENTER_USER, pwd=config.VCENTER_PASSWORD, port=int(443)
    )
    atexit.register(connect.Disconnect, si)

    # List of identifiers to return
    all_instance_ids = []

    # Recovers VM identifiers
    for vm in _getAllVms(si):
        obj_id = int(vm.summary.config.name.split("_")[1])
        if obj_id not in all_instance_ids:
            all_instance_ids.append(obj_id)

    # Recovers vSwitch identifiers
    for vswitch in _getAllVSwitchs(si):
        obj_id = int(vswitch.name.split("_")[1])
        if obj_id not in all_instance_ids:
            all_instance_ids.append(obj_id)

    # Recovers PortsGroups identifiers
    for portsgroup in _getAllPortsGroups(si):
        obj_id = int(portsgroup.name.split("_")[1])
        if obj_id not in all_instance_ids:
            all_instance_ids.append(obj_id)

    return all_instance_ids


# Destroys all clones (VMs, vSwitches, PortsGroups) having 'instance_id' as scenario identifier
def deleteAllClones(instance_id):
    # Connection to the vCenter: creation of the service instance and registration with atexit (?)
    si = connect.SmartConnectNoSSL(
        host=config.VCENTER_HOST, user=config.VCENTER_USER, pwd=config.VCENTER_PASSWORD, port=int(443)
    )
    atexit.register(connect.Disconnect, si)

    # Recovers the host
    host = _getHost(si)

    # Recovers all the objects to be deleted
    vms_to_destroy = [
        vm
        for vm in _getAllVms(si)
        if int(vm.summary.config.name.split("_")[1]) == int(instance_id)
    ]
    vswitchs_to_destroy = [
        vs
        for vs in _getAllVSwitchs(si)
        if int(vs.name.split("_")[1]) == int(instance_id)
    ]
    portsgroups_to_destroy = [
        pg
        for pg in _getAllPortsGroups(si)
        if int(pg.name.split("_")[1]) == int(instance_id)
    ]

    # Destruction of VMs
    for vm in vms_to_destroy:
        # Small additional failsafe
        if "vCenter" not in vm.summary.config.name:
            # If the VM is turned on, it is turned off
            if format(vm.runtime.powerState) == "poweredOn":
                task = vm.PowerOffVM_Task()
                _wait_for_tasks(si, [task])
            # Then it is destroyed
            task = vm.Destroy_Task()
            _wait_for_tasks(si, [task])

    # Destruction of portgroups
    for pg in portsgroups_to_destroy:
        host.configManager.networkSystem.RemovePortGroup(pg.name)

    # Destruction of vswitchs
    for vs in vswitchs_to_destroy:
        host.configManager.networkSystem.RemoveVirtualSwitch(vs.name)

    return len(vms_to_destroy) + len(portsgroups_to_destroy) + len(vswitchs_to_destroy)
