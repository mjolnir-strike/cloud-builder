# Cloud Builder CLI

A Python-based CLI tool for cloud infrastructure management.

## Requirements

- Python 3.12+
- pyenv (recommended for Python version management)
- Virtual environment

## Local Setup

1. Set up Python environment:
```bash
pyenv install 3.12.9  # if not already installed
pyenv local 3.12.9
python -m venv .venv
source .venv/bin/activate
```

2. Install the package:
```bash
pip install -e .
```

## Usage

Basic command structure:
```bash
cloud-build <command> [options]
```

Available commands:
- `print`: Print the given text
  ```bash
  cloud-build print hello world
  ```

For help:
```bash
cloud-build --help
cloud-build print --help
```

## Development

This project follows the infrastructure standards defined in our organization:
- Python 3.12+ with strict type checking
- Click for CLI implementation
- Development in virtual environment
- Regular dependency updates
- Error handling best practices

## Security

- No sensitive data in version control
- Input validation
- Error handling
- Regular dependency updates
