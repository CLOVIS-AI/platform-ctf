# This terraform configuration is used to start the platform on a random free port, so it can be used for tests during review.

terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "2.15.0"
    }
  }
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

variable "secrets" {
  type = set(string)
}

variable "platform_port" {
  type = number
}

provider "docker" {
  host = "ssh://${var.deployment_user}@${var.deployment_host}:${var.deployment_port}"
}

resource "docker_container" "docker_image" {
  image = "registry.gitlab.com/rsr22/plateforme-ctf/web:${var.build_version}"
  name  = "docker_web_interface_${var.build_version}_main"
  env = var.secrets
  ports {
    internal = 8000
    external = var.platform_port
  }
  volumes {
    container_path = "/app/data"
    volume_name = "ctf-data-${var.build_version}"
  }
  volumes {
    container_path = "/app/logs"
    volume_name = "ctf-logs-${var.build_version}"
  }
}
