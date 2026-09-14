# BindAI API

REST API for the BindAI Framework.

The API exposes BindAI agents, workflows, projects, and background automation execution through HTTP endpoints.

## Requirements

- Python 3.12+
- BindAI
- FastAPI
- Uvicorn

## Authentication

API endpoints under `/api/v1` require a Bearer API key.

Set:

```text
BINDAI_API_KEY=your-api-key

## Deployment notes

- The API does not provide built-in rate limiting. Production deployments should place it behind an appropriate reverse proxy, API gateway, or rate-limiting layer.
- Application, project, and automation state is kept in process memory. Run the API with a single worker unless this state is managed externally.