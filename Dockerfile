FROM python:3.7.1-stretch

RUN apt-get update
RUN apt-get install -y slic3r povray git

COPY src/ /src/
RUN pip3 install -r /src/requirements.txt

CMD export TERM=xterm && python3 /src/main.py