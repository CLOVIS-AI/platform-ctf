#!/usr/bin/env bash

#
# CTF Platform by RSR, educational platform to try cyber-security challenges
# Copyright (C) 2022 ENSEIRB-MATMECA, Bordeaux-INP, RSR formation since 2018
# Supervised by Toufik Ahmed, tad@labri.fr
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

# This script builds all the generic VMs from their configuration.
# Running this script requires a valid vCenter configuration, see the secret.properties file.

set -x  # display all commands

for file in generics/generic-*
do
	packer build -force "$file/build.pkr.hcl"
done