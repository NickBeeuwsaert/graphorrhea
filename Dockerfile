FROM python:3.9-alpine

ARG extras
ARG dev=0

ENV POETRY_HOME=/opt/poetry \
    DEV_MODE="${dev}" \
    PATH=/opt/poetry/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN apk add --no-cache --virtual .poetry-deps build-base musl-dev python3-dev libffi-dev openssl-dev cargo curl && \
    curl -sSL -o /tmp/get-poetry.py https://raw.githubusercontent.com/python-poetry/poetry/1.1.4/get-poetry.py && \
    echo "e973b3badb95a916bfe250c22eeb7253130fd87312afa326eb02b8bdcea8f4a7  /tmp/get-poetry.py" | sha256sum -c - && \
    POETRY_VERSION="1.1.4" python3 /tmp/get-poetry.py && \
    rm /tmp/get-poetry.py && \
    poetry self update && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root $([ "$DEV_MODE" = "0" ] && echo "--no-dev") ${extras:+-E "${extras}"} && \
    apk del .poetry-deps

COPY src src

RUN poetry install --no-interaction --no-ansi $([ "$DEV_MODE" = "0" ] && echo "--no-dev")

CMD pserve $([ "$DEV_MODE" = "0" ] && echo "production.ini" || echo "--reload development.ini")
