FROM ubuntu:bionic

RUN apt-get update
RUN apt-get install -y slic3r python python-pip povray g++ make

COPY src/ /src/
RUN pip install -r /src/requirements.txt
RUN cd /src/stl2pov && make && make install && apt-get purge -y g++ make

CMD export TERM=xterm && cd /src && python main.py