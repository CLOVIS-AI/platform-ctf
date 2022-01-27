#!/bin/sh

/usr/sbin/sshd -D &
/usr/sbin/apache2ctl -D FOREGROUND
