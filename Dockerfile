FROM python:3.6
MAINTAINER harumonia
WORKDIR /Poirot
USER root

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.4

RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get clean \
  && apt-get update -y \
  && apt-get -y install tesseract-ocr \
  && apt-get install -y libtesseract-dev \
  && apt-get -y install tesseract-ocr-chi-sim

COPY pyproject.toml /Poirot/

#-------国内用户可以反转以下语句以提高构建速度-------
RUN pip install --upgrade pip && pip install poetry
# RUN pip install --upgrade pip -i https://pypi.douban.com/simple
# RUN pip install poetry -i https://pypi.douban.com/simple
# RUN poetry config repositories.douban https://pypi.douban.com/simple/
# --------------------END---------------------

# use douban packages when build on local pc, but it will cause a error on docker hub.
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# COPY poetry.lock pyproject.toml /Poirot/
# RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

COPY . /Poirot
RUN mkdir -p /logs/gunicorn/ && chmod 777 /logs/gunicorn/
ENTRYPOINT  ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]
# ENTRYPOINT ["flask","run","--host","0.0.0.0"]
