FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl gcc libpq-dev \
    && apt-get clean

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

COPY ./poetry.lock ./pyproject.toml /app/

RUN poetry install --no-interaction

RUN mkdir app

COPY ./app /app/app

COPY ./web_sr.py /app

EXPOSE 8081

CMD ["poetry", "run", "uvicorn", "web_sr:app", "--host", "0.0.0.0", "--port", "8081"]
