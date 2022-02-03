ARG DOCKER_PROXY
FROM $DOCKER_PROXY/php:7.4-apache

#Fichiers site web
WORKDIR /var/www/html/
COPY index.html .
COPY ch1.html .
COPY ch2.html .
COPY ch3.html .

#Apache
COPY ./apache.conf /etc/apache2/sites-available/000-default.conf
RUN sed -i "s/AllowOverride None/AllowOverride All/g" /etc/apache2/apache2.conf
RUN echo "Yes, do as I say!" | a2dismod autoindex
RUN service apache2 restart

CMD ["/usr/sbin/apache2ctl","-D","FOREGROUND"]
