#!/bin/sh

/usr/sbin/apache2ctl start
/usr/sbin/sshd -D &
/etc/service/vsftpd/run
