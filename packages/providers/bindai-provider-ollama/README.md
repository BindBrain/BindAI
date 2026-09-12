# bindai-provider-ollama

Ollama provider for the BindAI framework.

## Installation

```bash
pip install "bindai[ollama]"
```

Or install the provider directly:

```bash
pip install bindai-provider-ollama
```

## Configuration

Make sure Ollama is running locally, then configure your BindAI project:

```toml
provider = "ollama"
model = "llama3.2"
```

By default, BindAI uses the local Ollama endpoint:

```env
OLLAMA_HOST=http://localhost:11434
```

## License

MIT