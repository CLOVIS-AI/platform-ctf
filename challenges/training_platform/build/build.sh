#!/usr/bin/env sh

challenge_name=training_platform

docker -H "ssh://$ssh_docker_user@$ssh_docker_hostname:$ssh_docker_port" build -t $challenge_name "$server_challenges"/$challenge_name/build
