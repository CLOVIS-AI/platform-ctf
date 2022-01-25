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


# region site

resource "docker_container" "docker_image" {
  image = "registry.gitlab.com/rsr22/plateforme-ctf/js_manipulation:${var.build_version}"
  name  = "docker_${var.instance_id}_js_manipulation"
  ports {
      internal = 80
    }
}

# endregion


#region Variables

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

output "port" {
  value = docker_container.docker_image.ports[0].external
}

# endregion
