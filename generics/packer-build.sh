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

set -x  # verbose mode

cache_file="$HOME/.cache/previous-packer-builds.csv"
mkdir -p "$(dirname "$cache_file")"
touch "$cache_file"

version_file="version.txt"
build_file="build.pkr.hcl"
prebuild_file="./prepare-build.sh"

version="$(cat $version_file)"
current_generic="$(basename "$(pwd)")"

existing="$(<"$cache_file" grep "$current_generic,$version" | cut -d ',' -f 3)"

if [[ -z $existing ]]; then
	# This version has not been recorded yet, build it
	test -f $prebuild_file && $prebuild_file
	packer build -force $build_file && echo "$current_generic,$version,$build_version" >>"$cache_file"
else
	# This version has already been recorded as version '$existing'
	echo "$current_generic has not been modified since the last build, using version $existing (version $version of Packer file)"
fi
