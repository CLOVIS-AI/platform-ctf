#!/bin/bash

/usr/local/nginx/sbin/nginx
/root/run_ffmpeg.sh &
/usr/sbin/sshd -D
