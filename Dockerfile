FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir uv

RUN uv sync --frozen

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "bindai_api.app:app", "--host", "0.0.0.0", "--port", "8000"]