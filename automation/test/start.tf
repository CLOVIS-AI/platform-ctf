# This terraform configuration is used to start the platform on a random free port, so it can be used for tests during review.

terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "2.15.0"
    }
  }
}

provider "docker" {
  host = "ssh://${var.deployment_user}@${var.deployment_host}:${var.deployment_port}"
}

resource "docker_container" "docker_image" {
  image = "registry.gitlab.com/rsr22/plateforme-ctf/web:${var.build_version}"
  name  = "docker_${var.instance_id}_web_interface"
  ports {
    internal = 8000
  }
}

variable "instance_id" {
  type = number
}

variable "deployment_user" {
  type = string
}

variable "deployment_port" {
  type = string
}

variable "deployment_host" {
  type = string
}

variable "build_version" {
  type = string
}

output "port" {
  value = docker_container.docker_image.ports[0].external
}
