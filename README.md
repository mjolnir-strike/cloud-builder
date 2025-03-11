# Cloud Builder CLI

A Python-based CLI tool for analyzing infrastructure code using AI agents.

## Features

- Terraform code analysis using AI agents
- Infrastructure best practices validation
- Security standards assessment
- Architecture review
- Cost optimization suggestions

## Requirements

- Python 3.12+
- pyenv (recommended for Python version management)
- Virtual environment
- OpenAI API key

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

3. Configure environment:
```bash
cp .env.template .env
# Edit .env and add your OpenAI API key
```

## Usage

Basic command structure:
```bash
cloud-build <command> [options]
```

Available commands:

1. Analyze Terraform code:
```bash
cloud-build analyze <directory> [--agent crew|langchain]
```
This will analyze your Terraform code for:
- Resource configuration best practices
- Security standards
- Infrastructure design patterns
- Cost optimization opportunities

2. Print text (utility command):
```bash
cloud-build print <text>
```

For help:
```bash
cloud-build --help
cloud-build analyze --help
```

## Analysis Features

The tool analyzes infrastructure code focusing on:

1. Resource Configuration:
   - Instance types and sizing
   - Storage configurations
   - Network architecture
   - Service integrations

2. Security Standards:
   - Access management
   - Network security
   - Service endpoints
   - Authentication methods

3. Infrastructure Design:
   - Resource organization
   - Module structure
   - Variable management
   - State configuration

4. Cost Optimization:
   - Resource efficiency
   - Scaling approach
   - Storage choices
   - Network design

## Development

This project follows infrastructure best practices:
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
- Environment-based configuration

## Dependencies

Core dependencies:
- crewai>=0.1.0 (primary)
- langchain>=0.1.0 (optional)
- pydantic>=2.0.0
- python-dotenv>=1.0.0
