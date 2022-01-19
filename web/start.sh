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

#
# This script is executed when the container starts.
#

date

set -x  # verbose mode
set -e  # abort if any command fails
set -u  # fail if we try to read an unset variable
set -o pipefail

app=/app

# Flask uses C-compiled binaries, which must be recompiled at container startup (why?)
source $app/venv/bin/activate
pip install -r $app/requirements.txt

#region SSH
# If the private key is available, load it
if [[ -n "$ssh_private_key" ]]
then
	mkdir -p /root/.ssh
	echo "$ssh_private_key" | base64 -d >/root/.ssh/id_rsa
	echo >>/root/.ssh/id_rsa
	chmod 400 /root/.ssh/id_rsa
	ssh-keygen -f /root/.ssh/id_rsa -y >/root/.ssh/id_rsa.pub  # Generate a public key from the private key
fi

[[ -n $ssh_vpn_fingerprint ]] && echo "$ssh_vpn_fingerprint" | base64 -d >>/root/.ssh/known_hosts
[[ -n $ssh_docker_fingerprint ]] && echo "$ssh_docker_fingerprint" | base64 -d >>/root/.ssh/known_hosts
#endregion

#region Migrations
# The database is created only the first time.
if [ ! -f "$database_file" ] && [ ! -d "$server_migrations" ]; then
    flask db init -d "$server_migrations"
fi

# Apply the migrations
flask db migrate -d "$server_migrations"
flask db upgrade -d "$server_migrations"

flask challenge import --all || true
flask help import --all || true
flask user create -u "$admin_user" -p "$admin_password" -m "$admin_email" --admin
flask crontab add
#endregion

# Start the cron daemon
/usr/sbin/crond

exec gunicorn \
	-w "$server_workers" \
	-b 0.0.0.0:8000 \
	--log-level="$server_log_level" \
	--log-file="$server_log_file" \
	--timeout="$server_timeout" \
	app:app
