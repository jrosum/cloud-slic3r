FROM ubuntu:bionic

# Set the locale
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN apt-get update
RUN apt-get install -y slic3r python3 python3-pip povray git

COPY src/ /src/
RUN export LANG="en_US.UTF-8" && pip3 install -r /src/requirements.txt

CMD export TERM=xterm && cd /src && python3 main.py