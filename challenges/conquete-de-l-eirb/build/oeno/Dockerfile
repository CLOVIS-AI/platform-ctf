ARG DOCKER_PROXY
FROM $DOCKER_PROXY/pensiero/apache-php:php7.4

RUN apt-get update && apt-get install -y openssh-server sudo vim

#Serveurs SSH
RUN useradd -rm -d /home/Pr3zOen0 -s /bin/bash -u 1001 Pr3zOen0 
RUN echo 'Pr3zOen0:BB_Zombie_Krot' | chpasswd
RUN service ssh start

#PrivEsc
RUN echo 'Pr3zOen0 ALL=(ALL) NOPASSWD: /usr/bin/vim' | sudo EDITOR='tee -a' visudo

#Fichiers site web
COPY ./public_html /var/www/html
COPY creds.txt /var/www/
RUN rm /var/www/html/index.html

#Apache
COPY ./apache.conf /etc/apache2/sites-available/000-default.conf
RUN sed -i "s/AllowOverride None/AllowOverride All/g" /etc/apache2/apache2.conf
RUN echo "Yes, do as I say!" | a2dismod autoindex
RUN service apache2 restart

# Start
COPY start.sh /root/start.sh
RUN chmod +x /root/start.sh
CMD ["/root/start.sh"]
