# BindAI Groq Provider

Groq provider integration for the BindAI framework.

## Installation

```bash
pip install "bindai[groq]"
```

Or install the provider directly:

```bash
pip install bindai-provider-groq
```

## Configuration

Set your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
```

Then configure your BindAI project:

```toml
provider = "groq"
model = "openai/gpt-oss-120b"
```

Use a model ID currently available from Groq's model catalog.

## Supported Provider Name

```text
groq
```

## License

MIT