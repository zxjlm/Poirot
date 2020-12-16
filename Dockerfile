FROM ubuntu:18.04
MAINTAINER harumonia
WORKDIR /Project/Poirot
USER root

COPY ./requirements.txt ./requirements.txt
COPY ./start.sh ./start.sh
COPY ./source_files ./source_files

RUN chmod 777 /etc/apt/sources.list && cat source_files/ubuntu > /etc/apt/sources.list && apt update && apt upgrade -y && apt-get install fontforge -y --no-install-recommends && apt-get install python3-pip -y

RUN chmod 777 ./start.sh && ./start.sh

COPY . .
RUN mkdir -p /logs/gunicorn/ && chmod 777 /logs/gunicorn/ && mkdir ./font_collection && mkdir ./fontforge_output
#RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
ENTRYPOINT  ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]
#ENTRYPOINT ["flask","run","--host","0.0.0.0"]
