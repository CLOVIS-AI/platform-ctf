#!/usr/bin/env sh

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

set -ex

echo http://dl-cdn.alpinelinux.org/alpine/v"$(</etc/alpine-release cut -d'.' -f1,2)"/main >>/etc/apk/repositories
echo http://dl-cdn.alpinelinux.org/alpine/v"$(</etc/alpine-release cut -d'.' -f1,2)"/community >>/etc/apk/repositories

apk update

apk add python2
apk add libressl
apk add open-vm-tools
apk add open-vm-tools-guestinfo
apk add open-vm-tools-deploypkg
rc-update add open-vm-tools
/etc/init.d/open-vm-tools start

echo '#!/usr/bin/env sh' >>/usr/local/bin/shutdown
echo 'poweroff' >>/usr/local/bin/shutdown

sed -i "/#PermitRootLogin/c\PermitRootLogin yes" /etc/ssh/sshd_config
/etc/init.d/sshd restart
