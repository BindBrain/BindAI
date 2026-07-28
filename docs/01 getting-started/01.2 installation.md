# Installation

This guide walks you through installing BindAI and preparing your development environment.

---

# Requirements

Before installing BindAI, make sure you have:

* Python 3.11 or newer
* pip
* Git (recommended)

You can verify your Python version:

```bash
python --version
```

---

# Clone the Repository

Clone the BindAI repository.

```bash
git clone https://github.com/bindbrain/bindai.git
```

Enter the project directory.

```bash
cd bindai
```

---

# Create a Virtual Environment

It is recommended to isolate your Python dependencies.

Windows

```powershell
python -m venv .venv

.venv\Scripts\activate
```

Linux / macOS

```bash
python -m venv .venv

source .venv/bin/activate
```

After activation, your terminal should display the virtual environment name.

Example:

```text
(.venv)
```

---

# Install BindAI

Install all local packages in editable mode.

```bash
pip install -e .
```

If you're developing the framework itself, editable mode ensures that changes to the source code are immediately available without reinstalling.

---

# Verify the Installation

You can verify the installation by importing BindAI.

```bash
python
```

```python
import bindai
```

If no errors occur, the installation was successful.

Exit Python.

```python
exit()
```

---

# Configure Environment Variables

Many AI providers require an API key.

Create a `.env` file in your project root.

Example:

```text
OPENAI_API_KEY=your_api_key_here
```

BindAI automatically loads environment variables when supported providers are used.

---

# Install Provider Packages

BindAI separates model providers into independent packages.

For example:

OpenAI

```bash
pip install bindai-openai
```

Anthropic

```bash
pip install bindai-anthropic
```

Google Gemini

```bash
pip install bindai-google
```

Ollama

```bash
pip install bindai-ollama
```

You only need to install the providers you intend to use.

---

# Install Optional Packages

Some BindAI features require optional packages.

Examples include:

* Vector databases
* Memory providers
* Document loaders
* Embedding providers

Install only the packages needed for your application.

---

# Running an Example

The repository includes example templates.

Run one of the examples:

```bash
python templates/agent-basic/main.py
```

If everything is configured correctly, the agent should execute and return a response from the configured AI provider.

---

# Common Issues

## ModuleNotFoundError

Ensure that the virtual environment is activated.

Reinstall the project if necessary.

```bash
pip install -e .
```

---

## Missing API Key

If the provider reports an authentication error, verify that the required environment variable exists.

Example:

```text
OPENAI_API_KEY=...
```

---

## Python Version

BindAI targets modern Python versions.

Verify your installation:

```bash
python --version
```


