ARG DOCKER_PROXY
FROM $DOCKER_PROXY/kalilinux/kali-rolling:latest
ENV DEBIAN_FRONTEND noninteractive

RUN apt update && apt -y install nmap iproute2 net-tools ssh wget nano
RUN service ssh start
RUN useradd -m -s /bin/bash -p $(openssl passwd -1 kali) kali
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
