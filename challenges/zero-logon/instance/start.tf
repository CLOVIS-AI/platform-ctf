#                                                    /===-_---~~~~~~~~~------____
#                                                    |===-~___                _,-'
#                     -==\\                         `//~\\   ~~~~`---.___.-~~
#                 ______-==|                         | |  \\           _-~`
#           __--~~~  ,-/-==\\                        | |   `\        ,'
#        _-~       /'    |  \\                      / /      \      /
#      .'        /       |   \\                   /' /        \   /'
#     /  ____  /         |    \`\.__/-~~ ~ \ _ _/'  /          \/'
#    /-'~    ~~~~~---__  |     ~-/~         ( )   /'        _--~`
#                      \_|      /        _)   ;  ),   __--~~
#                        '~~--_/      _-~/-  / \   '-~ \
#                       {\__--_/}    / \\_>- )<__\      \
#                       /'   (_/  _-~  | |__>--<__|      |
#                      |0  0 _/) )-~     | |__>--<__|     |
#                      / /~ ,_/       / /__>---<__/      |
#                     o o _//        /-~_>---<__-~      /
#                     (^(~          /~_>---<__-      _-~
#                    ,/|           /__>--<__/     _-~
#                 ,//('(          |__>--<__|     /                  .----_
#                ( ( '))          |__>--<__|    |                 /' _---_~\
#             `-)) )) (           |__>--<__|    |               /'  /     ~\`\
#            ,/,'//( (             \__>--<__\    \            /'  //        ||
#          ,( ( ((, ))              ~-__>--<_~-_  ~--____---~' _/'/        /'
#        `~/  )` ) ,/|                 ~-_~>--<_/-__       __-~ _/
#      ._-~//( )/ )) `                    ~~-'_/_/ /~~~~~~~__--~
#       ;'( ')/ ,)(                              ~~~~~~~~~~
#      ' ') '( (/
#        '   '  `
#    

#
# Variables
#
variable "instance_id" {
  type = string
}
variable "vcenter_host" {
  type = string
}
variable "vcenter_user" {
  type = string
}
variable "vcenter_password" {
  type = string
}
variable "vcenter_datastore" {
  type = string
}
variable "scenario_name" {
  type = string
  default = "zero_logon"
}


#
# Credentials vCenter
#
provider "vsphere" {
  password       = var.vcenter_password
  user           = var.vcenter_user
  vsphere_server = var.vcenter_host

  # If you have a self-signed cert
  allow_unverified_ssl = true
}

provider "time" {
}

#
# Datacenter, datastore, pool et host (là où on met les VM)
#
data "vsphere_datacenter" "dc" {
  name = "Datacenter"
}

data "vsphere_datastore" "datastore" {
  name          = var.vcenter_datastore
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_resource_pool" "pool" {
  name          = "Resources"
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_host" "host" {
  datacenter_id = data.vsphere_datacenter.dc.id
}


#
# Le réseau de base des VMs (celui de la salle RSR)
#
data "vsphere_network" "vm_network" {
  name          = "PLATEFORME_VM_OFFLINE"
  datacenter_id = data.vsphere_datacenter.dc.id
}

#
# Le nouveau switch qu'on crée pour le LAN et son réseau
#
resource "vsphere_host_virtual_switch" "sw_demo_LAN" {
  name           = "clonesw_${var.instance_id}_${var.scenario_name}"
  host_system_id = data.vsphere_host.host.id

  network_adapters = []

  active_nics  = []
  standby_nics = []
}

resource "vsphere_host_port_group" "pg_network_LAN_scenario" {
  name                = "clonepg_${var.instance_id}_${var.scenario_name}"
  host_system_id      = data.vsphere_host.host.id
  virtual_switch_name = vsphere_host_virtual_switch.sw_demo_LAN.name
}

resource "time_sleep" "wait_10_seconds" {
  create_duration = "10s"
  depends_on = [vsphere_host_port_group.pg_network_LAN_scenario]
}

data "vsphere_network" "network_LAN_scenario" {
  name          = "clonepg_${var.instance_id}_${var.scenario_name}"
  datacenter_id = data.vsphere_datacenter.dc.id
  depends_on = [
    vsphere_host_port_group.pg_network_LAN_scenario,
    time_sleep.wait_10_seconds
  ]
}


# region VM 1 - Pfsense


# Template
data "vsphere_virtual_machine" "template_clone_paul_demo_pfsense" {
  name          = "model_${var.scenario_name}_pfsense"
  datacenter_id = data.vsphere_datacenter.dc.id
}

# Création de la VM
resource "vsphere_virtual_machine" "vm_pfsense" {
  name             = "clonevm_${var.instance_id}_${var.scenario_name}_pfsense"
  resource_pool_id = data.vsphere_resource_pool.pool.id
  datastore_id     = data.vsphere_datastore.datastore.id

  folder = "plateforme-rsr/clones"

  # Bien tout garder à l'identique sinon le pfSense ne boot pas
  num_cpus = data.vsphere_virtual_machine.template_clone_paul_demo_pfsense.num_cpus
  memory   = data.vsphere_virtual_machine.template_clone_paul_demo_pfsense.memory
  guest_id = data.vsphere_virtual_machine.template_clone_paul_demo_pfsense.guest_id
  scsi_type = data.vsphere_virtual_machine.template_clone_paul_demo_pfsense.scsi_type

  # Première interface (WAN)
  network_interface {
    network_id   = data.vsphere_network.vm_network.id
    adapter_type = data.vsphere_virtual_machine.template_clone_paul_demo_pfsense.network_interface_types[0]
  }

  # Deuxième interface (LAN)
  network_interface {
    network_id   = data.vsphere_network.network_LAN_scenario.id
    adapter_type = data.vsphere_virtual_machine.template_clone_paul_demo_pfsense.network_interface_types[1]
  }

  disk {
    label            = "disk0"
    size             = data.vsphere_virtual_machine.template_clone_paul_demo_pfsense.disks.0.size
    eagerly_scrub    = data.vsphere_virtual_machine.template_clone_paul_demo_pfsense.disks.0.eagerly_scrub
    thin_provisioned = data.vsphere_virtual_machine.template_clone_paul_demo_pfsense.disks.0.thin_provisioned
  }

  # Clone lié pour économiser de la place
  clone {
    template_uuid = data.vsphere_virtual_machine.template_clone_paul_demo_pfsense.id
    linked_clone = true
  }

  # Sur le pfSense on attend l'ip au lieu du net (sinon ça boucle à l'infini)
  wait_for_guest_net_timeout = 0
  wait_for_guest_ip_timeout  = 3

  # On ignore son IP locale
  ignored_guest_ips = ["192.168.1.1"]
  
}

# endregion

# region VM 1 - Windows 10

# Template
data "vsphere_virtual_machine" "template_model_windows_10" {
  name          = "model_${var.scenario_name}_windows_10"
  datacenter_id = data.vsphere_datacenter.dc.id
}

# Création de la VM
resource "vsphere_virtual_machine" "vm_windows_10" {
  name             = "clonevm_${var.instance_id}_${var.scenario_name}_windows_10"
  resource_pool_id = data.vsphere_resource_pool.pool.id
  datastore_id     = data.vsphere_datastore.datastore.id

  folder = "plateforme-rsr/clones"

  num_cpus = 1
  memory   = 4096
  guest_id = data.vsphere_virtual_machine.template_model_windows_10.guest_id
  wait_for_guest_ip_timeout = -1
  wait_for_guest_net_timeout = -1

  network_interface {
    network_id   = data.vsphere_network.network_LAN_scenario.id
    adapter_type = data.vsphere_virtual_machine.template_model_windows_10.network_interface_types[0]
  }

  scsi_type = data.vsphere_virtual_machine.template_model_windows_10.scsi_type

  disk {
    label            = "disk0"
    size             = data.vsphere_virtual_machine.template_model_windows_10.disks.0.size
    eagerly_scrub    = data.vsphere_virtual_machine.template_model_windows_10.disks.0.eagerly_scrub
    thin_provisioned = data.vsphere_virtual_machine.template_model_windows_10.disks.0.thin_provisioned
  }

  clone {
    template_uuid = data.vsphere_virtual_machine.template_model_windows_10.id
    linked_clone = true
  }
  
}

# endregion

# region VM 2 - Windows Server

# Template
data "vsphere_virtual_machine" "template_model_windows_server" {
  name          = "model_${var.scenario_name}_windows_server"
  datacenter_id = data.vsphere_datacenter.dc.id
}

# Création de la VM
resource "vsphere_virtual_machine" "vm_windows_server" {
  name             = "clonevm_${var.instance_id}_${var.scenario_name}_windows_server"
  resource_pool_id = data.vsphere_resource_pool.pool.id
  datastore_id     = data.vsphere_datastore.datastore.id

  folder = "plateforme-rsr/clones"

  num_cpus = 1
  memory   = 4096
  guest_id = data.vsphere_virtual_machine.template_model_windows_server.guest_id
  wait_for_guest_ip_timeout = -1
  wait_for_guest_net_timeout = -1

  network_interface {
    network_id   = data.vsphere_network.network_LAN_scenario.id
    adapter_type = data.vsphere_virtual_machine.template_model_windows_server.network_interface_types[0]
  }

  scsi_type = data.vsphere_virtual_machine.template_model_windows_server.scsi_type

  disk {
    label            = "disk0"
    size             = data.vsphere_virtual_machine.template_model_windows_server.disks.0.size
    eagerly_scrub    = data.vsphere_virtual_machine.template_model_windows_server.disks.0.eagerly_scrub
    thin_provisioned = data.vsphere_virtual_machine.template_model_windows_server.disks.0.thin_provisioned
  }

  disk {
    unit_number      = 1
    label            = "disk1"
    size             = data.vsphere_virtual_machine.template_model_windows_server.disks.1.size
    eagerly_scrub    = data.vsphere_virtual_machine.template_model_windows_server.disks.1.eagerly_scrub
    thin_provisioned = data.vsphere_virtual_machine.template_model_windows_server.disks.1.thin_provisioned
  }

  clone {
    template_uuid = data.vsphere_virtual_machine.template_model_windows_server.id
    linked_clone = true
  }
  
}

# endregion

# region VM 3 - Kali

# Template
data "vsphere_virtual_machine" "template_model_kali" {
  name          = "model_${var.scenario_name}_kali"
  datacenter_id = data.vsphere_datacenter.dc.id
}

# Création de la VM
resource "vsphere_virtual_machine" "vm_kali" {
  name             = "clonevm_${var.instance_id}_${var.scenario_name}_kali"
  resource_pool_id = data.vsphere_resource_pool.pool.id
  datastore_id     = data.vsphere_datastore.datastore.id

  folder = "plateforme-rsr/clones"

  num_cpus = 1
  memory   = 2048
  guest_id = data.vsphere_virtual_machine.template_model_kali.guest_id
  wait_for_guest_ip_timeout = -1
  wait_for_guest_net_timeout = -1

  network_interface {
    network_id   = data.vsphere_network.network_LAN_scenario.id
    adapter_type = data.vsphere_virtual_machine.template_model_kali.network_interface_types[0]
  }

  disk {
    label            = "disk0"
    size             = data.vsphere_virtual_machine.template_model_kali.disks.0.size
    eagerly_scrub    = data.vsphere_virtual_machine.template_model_kali.disks.0.eagerly_scrub
    thin_provisioned = data.vsphere_virtual_machine.template_model_kali.disks.0.thin_provisioned
  }

  clone {
    template_uuid = data.vsphere_virtual_machine.template_model_kali.id
    linked_clone = true
  }
  
}

# endregion

#
# Variables en sortie
#
output "ip_pfsense" {
  value = vsphere_virtual_machine.vm_pfsense.default_ip_address
  description = "IP du Pfsense"
}
