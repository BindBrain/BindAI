# bindai-provider-anthropic

Anthropic provider for the BindAI framework.

## Installation

```bash
pip install "bindai[anthropic]"
```

Or install the provider directly:

```bash
pip install bindai-provider-anthropic
```

## Configuration

Set your Anthropic API key:

```env
ANTHROPIC_API_KEY=your-api-key
```

Then configure your BindAI project:

```toml
provider = "anthropic"
model = "claude-sonnet-4-5"
```

## License

MIT