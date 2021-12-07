provider "docker" {
  host = "ssh://${var.dockeruser}@${var.dockerhost}:${var.dockerport}"
}

resource "docker_container" "docker_image" {
  image = "training_platform"
  name  = "docker_${var.instance_id}_training_platform"
  ports {
    internal = 80
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
