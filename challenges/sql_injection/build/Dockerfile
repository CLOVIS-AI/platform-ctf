ARG GITLAB_PROXY
FROM $GITLAB_PROXY/pensiero/apache-php-mysql:php7.4

RUN apt-get update -y
RUN apt-get -y install apt-utils

#Install netcat 
RUN apt-get -y install netcat netcat-traditional 

#Config mysql
ENV MYSQL_ROOT_PASSWORD Password123?

RUN echo "mysql-server mysql-server/root_password password ${MYSQL_ROOT_PASSWORD}" | debconf-set-selections
RUN echo "mysql-server mysql-server/root_password_again password ${MYSQL_ROOT_PASSWORD}" | debconf-set-selections
RUN apt-get -y install mysql-server php-mysql

#Fichiers site web
COPY ./challenge-rsr-web/challenge-rsr /var/www/challenge-rsr
RUN mkdir /var/www/bdd
COPY ./challenge-rsr-web/bdd /var/www/bdd
RUN rm /var/www/html/index.html

#Apache
COPY ./challenge-rsr-web/conf/php.ini /etc/php/7.4/apache2/php.ini
COPY ./challenge-rsr-web/conf/apache2.conf /etc/apache2/apache2.conf
COPY ./challenge-rsr-web/conf/000-default.conf /etc/apache2/sites-available/000-default.conf
COPY ./challenge-rsr-web/conf/envvars /etc/apache2/envvars
RUN service apache2 restart

#Config base de donnees
RUN service mysql start ; mysql -u root -p${MYSQL_ROOT_PASSWORD} -Bse "CREATE USER 'zayrrox' IDENTIFIED BY 'zayrrox';\
	CREATE DATABASE challenge;\
	GRANT ALL PRIVILEGES ON challenge.* TO 'zayrrox';\
	FLUSH PRIVILEGES;\
 	use challenge;\
	source /var/www/bdd/populate.sql;"

RUN /etc/init.d/mysql stop

RUN echo '[mysqld]' >> /etc/mysql/my.cnf
RUN echo 'secure-file-priv = ""' >> /etc/mysql/my.cnf

#Ajout permissions /tmp
RUN mkdir /var/www/challenge-rsr/tmp
RUN chmod 777 /var/www/challenge-rsr/tmp


COPY scripts/start.sh /root/start.sh
ENTRYPOINT ["/root/start.sh"]
