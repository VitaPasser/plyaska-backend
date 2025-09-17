FROM ghcr.io/astral-sh/uv:alpine
LABEL authors="vitapasser"

ADD ./uv.lock /app/uv.lock
ADD ./pyproject.toml /app/pyproject.toml
ADD ./.python-version /app/.python-version

WORKDIR /app
RUN uv sync --locked

ENTRYPOINT ["uv", "run", "python", "-m", "src.main"]