# bindai-provider-openrouter

OpenRouter provider for the BindAI framework.

## Installation

```bash
pip install "bindai[openrouter]"
```

Or install the provider directly:

```bash
pip install bindai-provider-openrouter
```

## Configuration

Set your OpenRouter API key:

```env
OPENROUTER_API_KEY=your-api-key
```

Then configure your BindAI project:

```toml
provider = "openrouter"
model = "openai/gpt-4o-mini"
```

## License

MIT