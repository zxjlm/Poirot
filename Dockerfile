FROM python:3.6.6-alpine3.7
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

RUN pip install --upgrade pip && pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml /Poirot/

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

COPY . /Poirot
RUN mkdir -p /logs/gunicorn/ && chmod 777 /logs/gunicorn/ && mkdir ./font_collection && mkdir ./fontforge_output
#ENTRYPOINT  ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]
ENTRYPOINT ["flask","run","--host","0.0.0.0"]
