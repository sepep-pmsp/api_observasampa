FROM python:3.9
FROM ubuntu:12.04

RUN apt-get update && \
      apt-get -y install sudo

RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo

USER docker

CMD ["sudo", "start_server.sh"]


