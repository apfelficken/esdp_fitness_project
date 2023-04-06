FROM python:3.11

RUN mkdir /server && apt-get update && apt-get install -y git libpq-dev postgresql-client
RUN pip install poetry

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

copy . /code
