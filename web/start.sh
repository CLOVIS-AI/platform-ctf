#!/usr/bin/env bash

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

# Load the secret environment variables
source $app/secret.properties

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

[[ -n $ssh_vpn_public_key ]] && echo "$ssh_vpn_public_key" | base64 -d >>/root/.ssh/known_hosts
[[ -n $ssh_docker_public_key ]] && echo "$ssh_docker_public_key" | base64 -d >>/root/.ssh/known_hosts
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