# textbrowser

A CLI tool that fetches web pages headlessly using Playwright and converts them to Markdown.

## Installation

```bash
# Install textbrowser
uv tool install https://github.com/eleqtrizit/textbrowser.git

# Install Playwright browsers (automatic on first use, or manual):
textbrowser --install-browsers

# Install system dependencies for headless operation (Linux only)
# This is required on headless servers and CI environments
playwright install-deps firefox
```

**Note:** Browsers are installed automatically on first use. Use `--install-browsers` to pre-install.

## Usage

### Fetch a URL and convert to Markdown

```bash
textbrowser https://example.com
```

### Save output to a file

```bash
textbrowser https://example.com -o output.md
```

### Read HTML from stdin

```bash
curl https://example.com | textbrowser
```

## Development

```bash
# Install dependencies
uv sync

# Run tests (excluding integration tests)
uv run pytest -m "not integration"

# Run integration tests
uv run pytest -m integration

# Format code
uv run autopep8 --in-place <file>
uv run isort <file>

# Lint
uv run flake8 .
```
