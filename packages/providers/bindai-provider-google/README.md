# bindai-provider-google

Google Gemini provider for the BindAI framework.

## Installation

```bash
pip install "bindai[google]"
```

Or install the provider directly:

```bash
pip install bindai-provider-google
```

## Configuration

Set your Google Gemini API key:

```env
GEMINI_API_KEY=your-api-key
```

Then configure your BindAI project:

```toml
provider = "google"
model = "gemini-2.5-flash"
```

## License

MIT