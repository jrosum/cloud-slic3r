FROM ubuntu:bionic

RUN apt-get update
RUN apt-get install -y slic3r python python-pip

COPY src/ /src/
RUN pip install -r /src/requirements.txt

CMD cd /src && python main.py