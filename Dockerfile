FROM ghcr.io/astral-sh/uv:alpine
LABEL authors="vitapasser"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ADD ./uv.lock /app/uv.lock
ADD ./pyproject.toml /app/pyproject.toml
ADD ./.python-version /app/.python-version
ADD ./src /app/src

WORKDIR /app

RUN uv sync --locked

CMD uv run python -m src.main