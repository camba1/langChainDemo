FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry==1.6.1 && poetry config virtualenvs.create false

WORKDIR /code

COPY ./pyproject.toml ./README.md ./poetry.lock* ./

COPY ./package[s] ./packages

RUN poetry install  --no-interaction --no-ansi --no-root --no-dev

COPY ./app ./app

RUN poetry install --no-interaction --no-ansi --no-dev


EXPOSE 8080

CMD exec uvicorn app.server:app --host 0.0.0.0 --port 8080
