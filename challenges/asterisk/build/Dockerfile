FROM ubuntu:14.04

RUN apt update && apt upgrade -y \
	&& apt install -y wget aptitude make perl libwww-perl sox mpg123


RUN wget https://downloads.asterisk.org/pub/telephony/asterisk/old-releases/asterisk-1.8.12.0-rc1.tar.gz
RUN tar xzvf asterisk-1.8.12.0-rc1.tar.gz

WORKDIR /asterisk-1.8.12.0-rc1/
RUN ./contrib/scripts/install_prereq install
RUN ./configure
RUN make && make install samples

WORKDIR /home
COPY manager.conf /etc/asterisk/manager.conf
COPY flag.txt .
COPY run.sh /


ENTRYPOINT ["/run.sh"]
