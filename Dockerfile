FROM python:3.11-alpine
LABEL maintainer="Jeter <jeter@gmail.com>"

RUN apk add --no-cache \
    build-base \
    postgresql-dev \
    tzdata \
    curl

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /apps

COPY . .

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

EXPOSE 3000

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
