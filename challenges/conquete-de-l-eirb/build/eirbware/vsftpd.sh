#!/bin/bash

set -e

ANON_ROOT=${ANON_ROOT:-/home/anonymous/}
PASV_MAX_PORT=${PASV_MAX_PORT:-65515}
PASV_MIN_PORT=${PASV_MIN_PORT:-65500}
PASV_ADDRESS=${PASV_ADDRESS:-}
MAX_CLIENTS=${MAX_CLIENTS:-50}
ANON_MAX_RATE=${ANON_MAX_RATE:-6250000}
FTPD_BANNER=${FTPD_BANNER:-"Welcome to the Eirbware FTP Server"}
BANNER_FILE=${BANNER_FILE:-""}


[ -f /etc/vsftpd.conf ] || cat <<EOF > /etc/vsftpd.conf
listen=YES
anonymous_enable=YES
no_anon_password=YES
anon_max_rate=30000
dirmessage_enable=YES
hide_file={.ssh}
use_localtime=YES
connect_from_port_20=YES
secure_chroot_dir=/var/run/vsftpd/empty
write_enable=NO
seccomp_sandbox=NO
xferlog_std_format=NO
log_ftp_protocol=YES
syslog_enable=YES
hide_ids=YES
seccomp_sandbox=NO
pasv_enable=YES
port_enable=YES
anon_root=${ANON_ROOT}
pasv_max_port=${PASV_MAX_PORT}
pasv_min_port=${PASV_MIN_PORT}
max_clients=${MAX_CLIENTS}
anon_max_rate=${ANON_MAX_RATE}
ftpd_banner=${FTPD_BANNER}
banner_file=${BANNER_FILE}
pasv_address=${PASV_ADDRESS}
EOF

exec /usr/sbin/vsftpd