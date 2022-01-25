#!/bin/sh

#echo FLAG{lache_un_poce_bleu} > /home/flag.txt

service mysql start
/usr/sbin/apache2ctl -D FOREGROUND

