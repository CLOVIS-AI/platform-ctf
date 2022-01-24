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

# region cqteirb-kali

resource "docker_container" "docker_kali_image" {
  # using rtmp interception kali image
  image = "registry.gitlab.com/rsr22/plateforme-ctf/rtmp-interception-kali:${var.build_version}"
  name  = "docker_${var.instance_id}_kali_cqteirb"
  ports {
    internal = 22
  }
  networks_advanced {
    name = docker_network.docker_private_network_main.name
  }
}

# endregion

# region cqteirb-oeno

resource "docker_container" "docker_image_cqteirb-oeno" {
  image = "registry.gitlab.com/rsr22/plateforme-ctf/cqteirb-oeno:${var.build_version}"
  name  = "docker_${var.instance_id}_cqteirb-oeno"
  upload {
    file    = "/home/Pr3zOen0/user.txt"
    content = random_string.flag_cqteirb_oeno_user.result
  }
  upload {
    file    = "/root/root.txt"
    content = random_string.flag_cqteirb_oeno_root.result
  }
  networks_advanced {
    name = docker_network.docker_private_network_main.name
  }
}

# Génération du flag user 
resource "random_string" "flag_cqteirb_oeno_user" {
  keepers     = { instance_id = "${var.instance_id}_cqteirb_oeno_user" }
  length      = 16
  special     = false
  min_upper   = 4
  min_lower   = 4
  min_numeric = 4
  provisioner "local-exec" {
    command = "mkdir -p ${path.module}/flags; echo ${random_string.flag_cqteirb_oeno_user.result} > ${path.module}/flags/flag_cqteirb_oeno_user.txt"
  }
}

# Génération du flag root 
resource "random_string" "flag_cqteirb_oeno_root" {
  keepers     = { instance_id = "${var.instance_id}_cqteirb_oeno_root" }
  length      = 16
  special     = false
  min_upper   = 4
  min_lower   = 4
  min_numeric = 4
  provisioner "local-exec" {
    command = "mkdir -p ${path.module}/flags; echo ${random_string.flag_cqteirb_oeno_root.result} > ${path.module}/flags/flag_cqteirb_oeno_root.txt"
  }
}

# endregion

# region cqteirb-pixeirb

resource "docker_container" "docker_image_cqteirb-pixeirb" {
  image = "registry.gitlab.com/rsr22/plateforme-ctf/cqteirb-pixeirb:${var.build_version}"
  name  = "docker_${var.instance_id}_cqteirb-pixeirb"
  upload {
    file    = "/home/web_dev/user.txt"
    content = random_string.flag_cqteirb_pixeirb_user.result
  }
  upload {
    file    = "/root/root.txt"
    content = random_string.flag_cqteirb_pixeirb_root.result
  }
  networks_advanced {
    name = docker_network.docker_private_network_main.name
  }
}

# Génération du flag user
resource "random_string" "flag_cqteirb_pixeirb_user" {
  keepers     = { instance_id = "${var.instance_id}_cqteirb_pixeirb_user" }
  length      = 16
  special     = false
  min_upper   = 4
  min_lower   = 4
  min_numeric = 4
  provisioner "local-exec" {
    command = "mkdir -p ${path.module}/flags; echo ${random_string.flag_cqteirb_pixeirb_user.result} > ${path.module}/flags/flag_cqteirb_pixeirb_user.txt"
  }
}

# Génération du flag root
resource "random_string" "flag_cqteirb_pixeirb_root" {
  keepers     = { instance_id = "${var.instance_id}_cqteirb_pixeirb_root" }
  length      = 16
  special     = false
  min_upper   = 4
  min_lower   = 4
  min_numeric = 4
  provisioner "local-exec" {
    command = "mkdir -p ${path.module}/flags; echo ${random_string.flag_cqteirb_pixeirb_root.result} > ${path.module}/flags/flag_cqteirb_pixeirb_root.txt"
  }
}

# endregion

# region cqteirb-eirbware

resource "docker_container" "docker_image_cqteirb-eirbware" {
  image = "registry.gitlab.com/rsr22/plateforme-ctf/cqteirb-eirbware:${var.build_version}"
  name  = "docker_${var.instance_id}_cqteirb-eirbware"
  upload {
    file    = "/root/root.txt"
    content = random_string.flag_cqteirb_eirbware.result
  }
  networks_advanced {
    name = docker_network.docker_private_network_main.name
  }
  networks_advanced {
    name = docker_network.docker_private_network_voip.name
  }
}

# Génération du flag
resource "random_string" "flag_cqteirb_eirbware" {
  keepers     = { instance_id = "${var.instance_id}_cqteirb-eirbware" }
  length      = 16
  special     = false
  min_upper   = 4
  min_lower   = 4
  min_numeric = 4
  provisioner "local-exec" {
    command = "mkdir -p ${path.module}/flags; echo ${random_string.flag_cqteirb_eirbware.result} > ${path.module}/flags/flag_cqteirb-eirbware.txt"
  }
}

# endregion

# region cqteirb-asterisk

resource "docker_container" "docker_image_cqteirb-asterisk" {
  image = "registry.gitlab.com/rsr22/plateforme-ctf/cqteirb-asterisk:${var.build_version}"
  name  = "docker_${var.instance_id}_cqteirb-asterisk"
  upload {
    file    = "/home/flag.txt"
    content = random_string.flag_cqteirb_asterisk.result
  }
  networks_advanced {
    name = docker_network.docker_private_network_voip.name
  }
}

# Génération du flag
resource "random_string" "flag_cqteirb_asterisk" {
  keepers     = { instance_id = "${var.instance_id}_cqteirb-asterisk" }
  length      = 16
  special     = false
  min_upper   = 4
  min_lower   = 4
  min_numeric = 4
  provisioner "local-exec" {
    command = "mkdir -p ${path.module}/flags; echo ${random_string.flag_cqteirb_asterisk.result} > ${path.module}/flags/flag_cqteirb-asterisk.txt"
  }
}

# endregion

# region cqteirb-eirb_fr

resource "docker_container" "docker_image_cqteirb-eirb_fr" {
  image      = "registry.gitlab.com/rsr22/plateforme-ctf/cqteirb-eirb_fr:${var.build_version}"
  name       = "docker_${var.instance_id}_cqteirb-eirb_fr"
  depends_on = [time_sleep.wait_10_seconds]
  upload {
    file   = "/var/www/html/index.html"
    source = "${path.module}/index.html"
  }
  networks_advanced {
    name = docker_network.docker_private_network_main.name
  }
}

resource "null_resource" "local_exec_cqteirb-eirb_fr" {
  triggers = { instance_id = "docker_${var.instance_id}_cqteirb-eirb_fr" }
  provisioner "local-exec" {
    command = "bash ${path.module}/ip_dynamic.sh ${docker_container.docker_image_cqteirb-oeno.network_data[0].ip_address} ${docker_container.docker_image_cqteirb-pixeirb.network_data[0].ip_address} ${docker_container.docker_image_cqteirb-eirbware.network_data[0].ip_address}"
  }
}

resource "time_sleep" "wait_10_seconds" {
  create_duration = "10s"
  depends_on      = [null_resource.local_exec_cqteirb-eirb_fr]
}

# endregion

# region Networks

resource "docker_network" "docker_private_network_main" {
  name = "docker_${var.instance_id}_main_subnet"
}

resource "docker_network" "docker_private_network_voip" {
  name = "docker_${var.instance_id}_voip_subnet"
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
  value = docker_container.docker_kali_image.ports[0].external
}


# endregion
