FROM python:3.7
MAINTAINER harumonia
WORKDIR /Project/Poirot
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple
COPY . .
RUN mkdir -p /logs/gunicorn/
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]