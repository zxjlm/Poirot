FROM ubuntu:18.04
MAINTAINER harumonia
WORKDIR /Project/Poirot
USER root

COPY ./requirements.txt ./requirements.txt
COPY ./start.sh ./start.sh
COPY ./source_files ./source_files

RUN chmod 777 /etc/apt/sources.list && cat source_files/ubuntu > /etc/apt/sources.list && apt update && apt upgrade -y

RUN ./start.sh

COPY . .
RUN mkdir -p /logs/gunicorn/
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]