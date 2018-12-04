FROM ubuntu:bionic

RUN apt-get update
RUN apt-get install -y slic3r python python-pip

COPY ./* /slic3r-frontend/
RUN pip install -r /slic3r-frontend/requirements.txt

CMD cd /slic3r-frontend && python main.py