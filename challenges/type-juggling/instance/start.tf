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

#
# Génération du flag
#
resource "random_string" "flag" {
  keepers = {instance_id = var.instance_id }
  length = 16
  special = false
  min_upper = 4
  min_lower = 4
  min_numeric = 4
  provisioner "local-exec" {
    command = "mkdir -p ${path.module}/flags; echo ${random_string.flag.result} > ${path.module}/flags/flag.txt"
  }
}

# Create a container
resource "docker_container" "docker_image" {
  image = "registry.gitlab.com/rsr22/plateforme-ctf/type-juggling/php:${var.build_version}"
  name  = "docker_${var.instance_id}_type_juggling"
  ports {
    internal = 80
  }
  upload {
    file = "/var/www/html/conf.php"
    content = "<?php\n\n$FLAG = '${random_string.flag.result}';\n"
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

output "port" {
  value = docker_container.docker_image.ports[0].external
}
