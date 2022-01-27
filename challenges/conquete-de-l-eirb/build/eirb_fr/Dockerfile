ARG GITLAB_PROXY
FROM $GITLAB_PROXY/pensiero/apache-php:php7.4

RUN apt-get update

#Fichiers site web
RUN rm /var/www/html/index.html

#Apache
COPY ./apache.conf /etc/apache2/sites-available/000-default.conf
RUN sed -i "s/AllowOverride None/AllowOverride All/g" /etc/apache2/apache2.conf
RUN echo "Yes, do as I say!" | a2dismod autoindex
RUN service apache2 restart

CMD ["/usr/sbin/apache2ctl","-D","FOREGROUND"]
