# Image menggunakan PHP 8.1.x + Web Server
FROM php:8.1-apache

# copy web content
COPY ./web/ /var/www/html/

# set ownership and permissions
# untuk kepemilikan ‘u’ dan ‘g’ sudah di set ke www-data, 
# dan hilangkan permission ‘w’ and ‘x’ untuk others.
RUN chown -R www-data:www-data /var/www/html/ \
    && chmod -R u=rwX,g=rX,o= /var/www/html/

# set working directory
WORKDIR /var/www/html

# import database
COPY redlock-db.sql /docker-entrypoint-initdb.d/redlock-db.sql

# install mysqli
RUN apt-get update -y && apt-get install -y libmariadb-dev 
RUN docker-php-ext-install mysqli



