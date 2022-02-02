ARG DOCKER_PROXY
FROM $DOCKER_PROXY/php:7.4-apache

WORKDIR /var/www/html
COPY index.php .
COPY --chown=www-data conf.php .
