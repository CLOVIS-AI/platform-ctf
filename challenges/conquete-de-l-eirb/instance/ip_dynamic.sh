#!/bin/bash

cp index.tpl.html index.html
sed -i 's~%IP_OENO%~'$1'~g' index.html;
sed -i 's~%IP_PIXEIRB%~'$2'~g' index.html;
sed -i 's~%IP_EIRBWARE%~'$3'~g' index.html;
