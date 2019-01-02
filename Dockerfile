FROM python:3.7.1-stretch

RUN apt-get update
RUN apt-get install -y slic3r povray git admesh

COPY src/ /src/
RUN pip3 install -r /src/requirements.txt

CMD export TERM=xterm && cd /src && python3 main.py