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
resource "docker_network" "docker_rtmp_interception_network" {
  name = "docker_${var.instance_id}_rtmp_interception_network"
}

resource "docker_container" "docker_camera_image" {
  image = "registry.gitlab.com/rsr22/plateforme-ctf/rtmp-interception:${var.build_version}"
  name  = "docker_${var.instance_id}_camera_rtmp_interception"
  networks_advanced {
    name = docker_network.docker_rtmp_interception_network.name
  }
}

resource "docker_container" "docker_kali_image" {
  image = "registry.gitlab.com/rsr22/plateforme-ctf/rtmp-interception-kali:${var.build_version}"
  name  = "docker_${var.instance_id}_kali_rtmp_interception"
  ports {
    internal = 22
  }
  networks_advanced {
    name = docker_network.docker_rtmp_interception_network.name
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
