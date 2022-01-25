ARG GITLAB_PROXY
FROM $GITLAB_PROXY/ubuntu:latest

ARG nginx_version=1.17.6
ARG files="files"
ARG user="camera"
ARG password="c@m3r4sshP@sSw0rD"
ENV DEBIAN_FRONTEND noninteractive
WORKDIR /root

RUN apt-get update && apt-get install -y git build-essential ffmpeg libpcre3 libpcre3-dev libssl-dev \
                                         zlib1g-dev wget nano vim openssh-server iproute2 net-tools

# Install nginx-rtmp-module
RUN git clone https://github.com/sergey-dryabzhinsky/nginx-rtmp-module.git
RUN wget https://nginx.org/download/nginx-$nginx_version.tar.gz
RUN tar -xf nginx-$nginx_version.tar.gz
RUN rm nginx-$nginx_version.tar.gz
RUN cd nginx-$nginx_version && ./configure --prefix=/usr/local/nginx --with-http_ssl_module --add-module=../nginx-rtmp-module && make && make install
COPY $files/nginx.conf /usr/local/nginx/conf/nginx.conf

# Adds a new user with no root permissions
RUN useradd -m -s /bin/bash -p $(openssl passwd -1 $password) $user

# Copies the flag video to /root folder to hide it from the reglar user
COPY $files/video-flag.mp4 .
COPY $files/run_ffmpeg.sh .
RUN chmod +x run_ffmpeg.sh
COPY $files/run_all.sh .
RUN chmod +x run_all.sh

EXPOSE 22
EXPOSE 1935
EXPOSE 8080
RUN service ssh start

# Runs the script to start the ssh, ffmpeg and nginx services
CMD ["/root/run_all.sh"]
