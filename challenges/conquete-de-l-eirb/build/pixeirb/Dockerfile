ARG DOCKER_PROXY
FROM $DOCKER_PROXY/orsolin/docker-php-5.3-apache

# Update & package install
RUN apt update && apt install -y sudo python

# Apache configuration
COPY ./apache.conf /etc/apache2/sites-available/000-default.conf

# Web site files & permissions
COPY ./public_html/ /var/www/html
RUN chown -R www-data:www-data /var/www
RUN chmod -R g+rwX /var/www

# Users & Privilege Escalation 
RUN useradd -rm -d /home/web_dev -s /bin/bash -u 1001 web_dev 
RUN groupadd webmaster
RUN usermod -aG webmaster www-data 
RUN usermod -aG webmaster web_dev 
COPY privesc/pam_permissions /etc/pam.d/su
RUN cp /sbin/getcap /usr/local/bin/
RUN setcap cap_setuid+ep /usr/local/bin/php
RUN setcap cap_net_raw+p /bin/ping
RUN setcap cap_net_raw+p /bin/ping6

# Start
COPY start.sh /root/start.sh
RUN chmod +x /root/start.sh
CMD ["/root/start.sh"]
