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

resource "docker_container" "docker_image" {
  image = "asterisk"
  name  = "docker_${var.instance_id}_asterisk"
  ports {
    internal = 5038
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

output "port" {
  value = docker_container.docker_image.ports[0].external
}
