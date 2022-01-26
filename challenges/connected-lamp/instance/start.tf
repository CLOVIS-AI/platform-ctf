terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "2.15.0"
    }
  }
}

provider "docker" {
  host = "ssh://${var.dockeruser}@${var.dockerhost}:${var.dockerport}"
}

# create a network containing the rtmp-interception instance and a kali instance
resource "docker_network" "docker_connected_lamp_network" {
  name = "docker_${var.instance_id}_connected_lamp_network"
}

resource "docker_container" "docker_connected_lamp" {
  image = "registry.gitlab.com/rsr22/plateforme-ctf/connected-lamp:${var.build_version}"
  name  = "docker_${var.instance_id}_connected_lamp"
  networks_advanced {
    name = docker_network.docker_connected_lamp_network.name
  }
  upload {
    file = "/home/flag.txt"
    content = random_string.flag.result
  }
}

resource "docker_container" "docker_kali_image" {
  # using rtmp interception kali image
  image = "registry.gitlab.com/rsr22/plateforme-ctf/rtmp-interception-kali:${var.build_version}"
  name  = "docker_${var.instance_id}_kali_connected_lamp"
  ports {
    internal = 22
  }
  networks_advanced {
    name = docker_network.docker_connected_lamp_network.name
  }
}

#
# Génération du flag
#
resource "random_string" "flag" {
  keepers = {instance_id = var.instance_id}
  length = 16
  special = false
  min_upper = 4
  min_lower = 4
  min_numeric = 4
  provisioner "local-exec" {
    command = "mkdir -p ${path.module}/flags; echo ${random_string.flag.result} > ${path.module}/flags/flag.txt"
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

output "port22_kali" {
  value = docker_container.docker_kali_image.ports[0].external
}
