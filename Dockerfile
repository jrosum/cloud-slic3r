FROM debian:stretch

RUN apt-get update
RUN apt-get install -y slic3r python3 python3-pip povray git

COPY src/ /src/
RUN pip3 install -r /src/requirements.txt

CMD export TERM=xterm && cd /src && python3 main.py