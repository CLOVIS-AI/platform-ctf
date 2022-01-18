variable "generic_password" {
  type    = string
  default = "${env("TF_VAR_generic_password")}"
}

variable "generic_user" {
  type    = string
  default = "${env("TF_VAR_generic_user")}"
}

variable "generic_root_user" {
  type    = string
  default = "${env("TF_VAR_generic_root_user")}"
}

variable "vcenter_datastore" {
  type    = string
  default = "${env("TF_VAR_vcenter_datastore")}"
}

variable "vcenter_host" {
  type    = string
  default = "${env("TF_VAR_vcenter_host")}"
}

variable "vcenter_network0" {
  type    = string
  default = "${env("TF_VAR_network0")}"
}

variable "vcenter_network0_card" {
  type    = string
  default = "${env("TF_VAR_network0_card")}"
}

variable "vcenter_password" {
  type    = string
  default = "${env("TF_VAR_vcenter_password")}"
}

variable "vcenter_user" {
  type    = string
  default = "${env("TF_VAR_vcenter_user")}"
}

variable "build_version" {
  type    = string
  default = "${env("build_version")}"
}

# "timestamp" template function replacement
locals { timestamp = regex_replace(timestamp(), "[- TZ:]", "") }

source "vsphere-iso" "autogenerated_1" {
  CPUs                 = 1
  RAM                  = 512
  RAM_reserve_all      = true
  boot_command         = ["${var.generic_root_user}<enter><wait>", "ifconfig eth0 up && udhcpc -i eth0<enter><wait5>", "mount -t vfat /dev/fd0 /media/floppy<enter><wait>", "printf \"${var.generic_password}\\n${var.generic_password}\\ny\\n\" | setup-alpine -f /media/floppy/answerfile ; reboot<enter>", "<wait120>", "${var.generic_root_user}<enter>", "${var.generic_password}<enter><wait>", "mount -t vfat /dev/fd0 /media/floppy<enter><wait>", "/media/floppy/SETUP.SH<enter>"]
  boot_wait            = "15s"
  datastore            = "${var.vcenter_datastore}"
  disk_controller_type = ["pvscsi"]
  floppy_files         = ["${path.root}/answerfile", "${path.root}/setup.sh"]
  guest_os_type        = "other3xLinux64Guest"
  host                 = "${var.vcenter_host}"
  insecure_connection  = "true"
  iso_checksum         = "sha256:17df5aaf6fad99e57767b51f6934ebb799b7e72e8bed8a5f1d4a0639899b7e9b"
  iso_url              = "https://dl-cdn.alpinelinux.org/alpine/v3.12/releases/x86_64/alpine-standard-3.12.1-x86_64.iso"
  network_adapters {
    network      = "${var.vcenter_network0}"
    network_card = "${var.vcenter_network0_card}"
  }
  password     = "${var.vcenter_password}"
  ssh_password = "${var.generic_password}"
  ssh_username = "${var.generic_root_user}"
  storage {
    disk_size             = 8192
    disk_thin_provisioned = true
  }
  username       = "${var.vcenter_user}"
  vcenter_server = "${var.vcenter_host}"
  vm_name        = "${var.build_version}-generic-alpine-3.12"
}

build {
  sources = ["source.vsphere-iso.autogenerated_1"]

  provisioner "shell" {
    inline = ["echo 'Installation done!'"]
  }
}
