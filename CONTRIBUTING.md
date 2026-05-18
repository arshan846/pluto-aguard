# Contributing to Pluto AgentGuard

Thank you for your interest in contributing! This guide will help you get started.

## Development Setup

### Prerequisites

- **Python 3.10+** — [Download](https://www.python.org/downloads/)
- **Git** — [Download](https://git-scm.com/downloads)

### Setup

```bash
# Clone the repository
git clone https://github.com/arpitha-dhanapathi/pluto-aguard.git
cd pluto-aguard

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run a specific test module
pytest tests/scanners/test_mcp_scanner.py -v

# Run with coverage
pytest tests/ --cov=pluto_aguard --cov-report=term-missing
```

### Linting

```bash
# Check for linting issues
ruff check src/

# Auto-fix linting issues
ruff check src/ --fix
```

## How to Contribute

### Reporting Bugs

Open an [issue](https://github.com/arpitha-dhanapathi/pluto-aguard/issues) with:
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS

### Adding Scanner Rules

1. Add your rule definition to `src/pluto_aguard/rules/owasp_mcp_top10.yaml`
2. Implement the check in the appropriate scanner module
3. Add tests in `tests/scanners/`
4. Submit a PR

### Adding Framework Adapters

To add support for a new agent framework (e.g., LangChain, CrewAI):
1. Create a new adapter in `src/pluto_aguard/monitor/adapters/`
2. Implement trace parsing for the framework's output format
3. Add tests and example traces
4. Submit a PR

## Code Style

- Follow [PEP 8](https://pep8.org/) conventions
- Use type hints for all function signatures
- Keep functions focused and under 50 lines where possible
- Add docstrings to all public functions and classes

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes with tests
4. Run `pytest` and `ruff check` to verify
5. Submit a PR with a clear description of what and why

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
