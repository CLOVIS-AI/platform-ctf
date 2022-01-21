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

data "vsphere_datacenter" "dc" {
  name = var.vcenter_datacenter
}

data "vsphere_datastore" "datastore" {
  name          = var.vcenter_datastore
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_host" "host" {
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_resource_pool" "pool" {
  name          = var.vcenter_resource_pool
  datacenter_id = data.vsphere_datacenter.dc.id
}

# Template
data "vsphere_virtual_machine" "original" {
  name          = "${var.original_build_version}-${var.generic_name}"
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_network" "vm_network" {
  name          = var.network0
  datacenter_id = data.vsphere_datacenter.dc.id
}

# Création de la VM
resource "vsphere_virtual_machine" "clone" {
  name             = "${var.new_build_version}-${var.generic_name}"
  resource_pool_id = data.vsphere_resource_pool.pool.id
  datastore_id     = data.vsphere_datastore.datastore.id

  num_cpus  = data.vsphere_virtual_machine.original.num_cpus
  memory    = data.vsphere_virtual_machine.original.memory
  guest_id  = data.vsphere_virtual_machine.original.guest_id
  scsi_type = data.vsphere_virtual_machine.original.scsi_type

  network_interface {
    network_id   = data.vsphere_network.vm_network.id
    adapter_type = data.vsphere_virtual_machine.original.network_interface_types[0]
  }

  disk {
    label            = "disk0"
    size             = data.vsphere_virtual_machine.original.disks.0.size
    eagerly_scrub    = data.vsphere_virtual_machine.original.disks.0.eagerly_scrub
    thin_provisioned = data.vsphere_virtual_machine.original.disks.0.thin_provisioned
  }

  clone {
    template_uuid = data.vsphere_virtual_machine.original.id
    linked_clone  = false
  }

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

variable "vcenter_datacenter" {
  type = string
}

variable "vcenter_resource_pool" {
  type = string
}

variable "network0" {
  type = string
}

variable "original_build_version" {
  type = string
}

variable "new_build_version" {
  type = string
}

variable "generic_name" {
  type = string
}
