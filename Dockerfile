FROM python:3.7.1-stretch

RUN apt-get update
RUN apt-get install -y slic3r povray git admesh curl

COPY src/ /src/
RUN pip3 install -r /src/requirements.txt

CMD export TERM=xterm && cd /src && gunicorn -b 0.0.0.0:8088 -w 6 main:app