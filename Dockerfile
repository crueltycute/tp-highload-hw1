FROM ubuntu:18.04

RUN apt-get -y update &&\
    apt-get -y upgrade &&\
    apt-get -y install python3

COPY . /src

EXPOSE 80

CMD python3 /src/main.py