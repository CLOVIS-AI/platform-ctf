ARG GITLAB_PROXY
FROM $GITLAB_PROXY/pensiero/apache-php:php7.4

RUN apt-get update && apt-get install -y openssh-server vsftpd iproute2 telnet netcat

#Serveur SSH
#RUN mkdir -p /root/.ssh/
RUN mkdir /root/.ssh/ \
 && ssh-keygen -t rsa -N "" -C "prez@eirbware" -f /root/.ssh/id_rsa \
 && mv /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys
RUN service ssh start

#Serveur FTP
RUN mkdir -p /var/run/vsftpd/empty \
 && mkdir -p /etc/vsftpd \
 && mkdir -p /var/ftp \
 && mv /etc/vsftpd.conf /etc/vsftpd.orig \
 && mkdir -p /etc/service/vsftpd

RUN mkdir -p /home/anonymous/.ssh
COPY ftp/* /home/anonymous/
COPY ftp/.creds.txt /home/anonymous/.creds.txt

RUN mv /root/.ssh/id_rsa /home/anonymous/.ssh/id_rsa \
 && chmod 777 /home/anonymous/.ssh/id_rsa

ADD vsftpd.sh /etc/service/vsftpd/run
RUN chmod +x /etc/service/vsftpd/run

#Fichiers site web
COPY ./public_html /var/www/html
RUN rm /var/www/html/index.html

#Apache
COPY ./apache.conf /etc/apache2/sites-available/000-default.conf
RUN sed -i "s/AllowOverride None/AllowOverride All/g" /etc/apache2/apache2.conf
RUN echo "Yes, do as I say!" | a2dismod autoindex
RUN service apache2 restart

#Hint pour la suite 
COPY hints/.secret.txt /root/
COPY hints/hint.txt /root/

#Start
COPY start.sh /root/.start.sh
RUN chmod +x /root/.start.sh
CMD ["/root/.start.sh"]