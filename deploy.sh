#!/usr/bin/env bash

#
# Downloads the container from the GitLab registry and starts it.
#
# This script is meant to run from a crontab, to automatically update a server.
# It is not meant for development.
#
# To use this script, you simply need:
# - the script itself,
# - the docker-compose.yml file,
# - the docker-compose.prod.yml file,
# - the web/secret.properties file.
#

set -x  # bash verbose mode

compose-prod=docker-compose -f docker-compose.yml -f docker-compose.prod.yml

git pull
$(compose-prod) pull
$(compose-prod) up -d
