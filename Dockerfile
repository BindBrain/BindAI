FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir uv \
    && uv sync --frozen \
    && useradd --create-home --shell /bin/bash bindai \
    && chown -R bindai:bindai /app

USER bindai

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "bindai_api.app:app", "--host", "0.0.0.0", "--port", "8000"]