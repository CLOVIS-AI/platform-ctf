terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "2.11.0"
    }
  }
}

provider "docker" {
  host = "ssh://${var.dockeruser}@${var.dockerhost}:${var.dockerport}"
}

resource "docker_network" "docker_network_link0" {
  name = "docker_${var.instance_id}_link0"
}

resource "docker_network" "docker_network_link1" {
  name = "docker_${var.instance_id}_link1"
}

resource "docker_network" "docker_network_link2" {
  name = "docker_${var.instance_id}_link2"
}

resource "docker_network" "docker_network_link3" {
  name = "docker_${var.instance_id}_link3"
}

resource "docker_network" "docker_network_link4" {
  name = "docker_${var.instance_id}_link4"
}

resource "docker_network" "docker_network_link5" {
  name = "docker_${var.instance_id}_link5"
}

resource "docker_image" "docker_image_cam0" {
  name = "registry.gitlab.com/rsr22/plateforme-ctf/camsafe/cam0:${var.build_version}"
}

resource "docker_image" "docker_image_cam1" {
  name = "registry.gitlab.com/rsr22/plateforme-ctf/camsafe/cam1:${var.build_version}"
}

resource "docker_image" "docker_image_cam2" {
  name = "registry.gitlab.com/rsr22/plateforme-ctf/camsafe/cam2:${var.build_version}"
}

resource "docker_image" "docker_image_web" {
  name = "registry.gitlab.com/rsr22/plateforme-ctf/camsafe/web:${var.build_version}"
}

resource "docker_image" "docker_image_routeur" {
  name = "registry.gitlab.com/rsr22/plateforme-ctf/camsafe/routeur:${var.build_version}"
}

resource "docker_image" "docker_image_camserv" {
  name = "registry.gitlab.com/rsr22/plateforme-ctf/camsafe/camserv:${var.build_version}"
}

#
# WEB
#
resource "random_string" "flag_web" {
  keepers = {instance_id = "${var.instance_id}_web"}
  length = 16
  special = false
  min_upper = 4
  min_lower = 4
  min_numeric = 4
  provisioner "local-exec" {
    command = "mkdir -p ${path.module}/flags; echo ${random_string.flag_web.result} > ${path.module}/flags/flag_web.txt"
  }
}

resource "docker_container" "docker_image_web" {
  image = docker_image.docker_image_web.latest
  name  = "docker_${var.instance_id}_camsafe_web"
  upload {
    file = "/var/www/html/uploads/flag.txt"
    content = random_string.flag_web.result
  }
  capabilities {
    add = ["NET_ADMIN"]
  }
  networks_advanced {
    name = docker_network.docker_network_link1.name
  }
}

#
# CAMSERV
#
resource "random_string" "flag_camserv" {
  keepers = {instance_id = "${var.instance_id}_camserv"}
  length = 16
  special = false
  min_upper = 4
  min_lower = 4
  min_numeric = 4
  provisioner "local-exec" {
    command = "mkdir -p ${path.module}/flags; echo ${random_string.flag_camserv.result} > ${path.module}/flags/flag_camserv.txt"
  }
}


resource "docker_container" "docker_image_camserv" {
  image = docker_image.docker_image_camserv.latest
  name  = "docker_${var.instance_id}_camsafe_camserv"
  upload {
    file = "/var/www/html/flag.txt"
    content = "FLAG: ${random_string.flag_camserv.result}\n"
  }
  upload {
    file = "/ip"
    content = docker_container.docker_image_routeur.network_data[0].gateway
  }
  upload {
    file = "/port"
    content = docker_container.docker_image_routeur.ports[1].external
  }
  capabilities {
    add = ["NET_ADMIN"]
  }
  networks_advanced {
    name = docker_network.docker_network_link2.name
  }
}

#
# ROUTEUR
#
resource "random_string" "flag_routeur" {
  keepers = {instance_id = "${var.instance_id}_routeur"}
  length = 16
  special = false
  min_upper = 4
  min_lower = 4
  min_numeric = 4
  provisioner "local-exec" {
    command = "mkdir -p ${path.module}/flags; echo ${random_string.flag_routeur.result} > ${path.module}/flags/flag_routeur.txt"
  }
}

resource "docker_container" "docker_image_routeur" {
  image = docker_image.docker_image_routeur.latest
  name  = "docker_${var.instance_id}_camsafe_routeur"
  ports {
    internal = 22
  }
  ports {
    internal = 80
  }
  ports {
    internal = 7777
  }
  upload {
    file = "/flag.txt"
    content = random_string.flag_routeur.result
  }
  capabilities {
    add = ["NET_ADMIN"]
  }
  networks_advanced {
    name = docker_network.docker_network_link0.name
  }
  networks_advanced {
    name = docker_network.docker_network_link1.name
  }
  networks_advanced {
    name = docker_network.docker_network_link2.name
  }
  networks_advanced {
    name = docker_network.docker_network_link3.name
  }
  networks_advanced {
    name = docker_network.docker_network_link4.name
  }
  networks_advanced {
    name = docker_network.docker_network_link5.name
  }
}

#
# CAM0
#
resource "random_string" "flag_cam0" {
  keepers = {instance_id = "${var.instance_id}_cam0"}
  length = 16
  special = false
  min_upper = 4
  min_lower = 4
  min_numeric = 4
  provisioner "local-exec" {
    command = "mkdir -p ${path.module}/flags; echo ${random_string.flag_cam0.result} > ${path.module}/flags/flag_cam0.txt"
  }
}

resource "random_string" "flag_cam0_root" {
  keepers = {instance_id = "${var.instance_id}_cam0"}
  length = 16
  special = false
  min_upper = 4
  min_lower = 4
  min_numeric = 4
  provisioner "local-exec" {
    command = "mkdir -p ${path.module}/flags; echo ${random_string.flag_cam0_root.result} > ${path.module}/flags/flag_cam0_root.txt"
  }
}

resource "docker_container" "docker_image_cam0" {
  image = docker_image.docker_image_cam0.latest
  name  = "docker_${var.instance_id}_camsafe_cam0"
  upload {
    file = "/home/camsafe/flag.txt"
    content = random_string.flag_cam0.result
  }
  upload {
    file = "/root/flag.txt"
    content = random_string.flag_cam0_root.result
  }
  upload {
    file = "/ip"
    content = docker_container.docker_image_routeur.network_data[0].gateway
  }
  upload {
    file = "/port"
    content = docker_container.docker_image_routeur.ports[1].external
  }
  capabilities {
    add = ["NET_ADMIN"]
  }
  networks_advanced {
    name = docker_network.docker_network_link3.name
  }
}

#
# CAM1
#
resource "random_string" "flag_cam1" {
  keepers = {instance_id = "${var.instance_id}_cam1"}
  length = 16
  special = false
  min_upper = 4
  min_lower = 4
  min_numeric = 4
  provisioner "local-exec" {
    command = "mkdir -p ${path.module}/flags; echo ${random_string.flag_cam1.result} > ${path.module}/flags/flag_cam1.txt"
  }
}

resource "random_string" "flag_cam1_root" {
  keepers = {instance_id = "${var.instance_id}_cam1"}
  length = 16
  special = false
  min_upper = 4
  min_lower = 4
  min_numeric = 4
  provisioner "local-exec" {
    command = "mkdir -p ${path.module}/flags; echo ${random_string.flag_cam1_root.result} > ${path.module}/flags/flag_cam1_root.txt"
  }
}


resource "docker_container" "docker_image_cam1" {
  image = docker_image.docker_image_cam1.latest
  name  = "docker_${var.instance_id}_camsafe_cam1"
  upload {
    file = "/home/camsafe/flag.txt"
    content = random_string.flag_cam1.result
  }
  upload {
    file = "/root/flag.txt"
    content = random_string.flag_cam1_root.result
  }
  upload {
    file = "/ip"
    content = docker_container.docker_image_routeur.network_data[0].gateway
  }
  upload {
    file = "/port"
    content = docker_container.docker_image_routeur.ports[1].external
  }
  capabilities {
    add = ["NET_ADMIN"]
  }
  networks_advanced {
    name = docker_network.docker_network_link4.name
  }
}

#
# CAM2
#
resource "random_string" "flag_cam2" {
  keepers = {instance_id = "${var.instance_id}_cam2"}
  length = 16
  special = false
  min_upper = 4
  min_lower = 4
  min_numeric = 4
  provisioner "local-exec" {
    command = "mkdir -p ${path.module}/flags; echo ${random_string.flag_cam2.result} > ${path.module}/flags/flag_cam2.txt"
  }
}

resource "random_string" "flag_cam2_root" {
  keepers = {instance_id = "${var.instance_id}_cam2"}
  length = 16
  special = false
  min_upper = 4
  min_lower = 4
  min_numeric = 4
  provisioner "local-exec" {
    command = "mkdir -p ${path.module}/flags; echo ${random_string.flag_cam2_root.result} > ${path.module}/flags/flag_cam2_root.txt"
  }
}



resource "docker_container" "docker_image_cam2" {
  image = docker_image.docker_image_cam0.latest
  name  = "docker_${var.instance_id}_camsafe_cam2"
  upload {
    file = "/home/camsafe/flag.txt"
    content = random_string.flag_cam2.result
  }
  upload {
    file = "/root/flag.txt"
    content = random_string.flag_cam2_root.result
  }
  upload {
    file = "/ip"
    content = docker_container.docker_image_routeur.network_data[0].gateway
  }
  upload {
    file = "/port"
    content = docker_container.docker_image_routeur.ports[1].external
  }
  capabilities {
    add = ["NET_ADMIN"]
  }
  networks_advanced {
    name = docker_network.docker_network_link5.name
  }
}


variable "instance_id" {
  type = number
}

variable "dockerhost" {
  type = string
}

variable "dockerport" {
  type = string
}

variable "dockeruser" {
  type = string
}

variable "build_version" {
  type = string
}

output "port22" {
  value = docker_container.docker_image_routeur.ports[0].external
}

output "port80" {
  value = docker_container.docker_image_routeur.ports[1].external
}

output "port7777" {
  value = docker_container.docker_image_routeur.ports[2].external
}

