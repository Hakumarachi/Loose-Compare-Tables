FROM ubuntu:xenial

RUN apt update && \
    apt install -y \
    flex \
    bison \
    build-essential \
    apache2 \
    apache2-dev \
    wget \
    libc6-dev

ARG PHP_VERSION
ARG PHP

RUN wget http://museum.php.net/${PHP}/php-${PHP_VERSION}.tar.bz2 || wget http://museum.php.net/${PHP}/php-${PHP_VERSION}.tar.gz

RUN tar xjf php-${PHP_VERSION}.tar.bz2 || tar xvf php-${PHP_VERSION}.tar.gz

WORKDIR /php-${PHP_VERSION}

RUN ./configure && make && make install

ENTRYPOINT ["/bin/bash"]