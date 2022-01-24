#!/bin/sh

chown web_dev:web_dev /home/web_dev/user.txt
chmod 660 /home/web_dev/user.txt
/usr/sbin/apache2ctl -D FOREGROUND
