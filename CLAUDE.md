# Smol Web Agents Project Guide

## Development Commands
- **Install Dependencies**: `uv pip install -e .`
- **Sync Dependencies**: `uv sync` (using uv.lock file)
- **Run Agent**: `python basic_web_agent.py`
- **Lint Code**: `ruff check .`
- **Type Check**: `mypy .`
- **Format Code**: `ruff format .`

## Code Style Guidelines
- **Imports**: Group standard library, third-party, and local imports separately
- **Formatting**: Follow PEP 8, line length max 88 characters
- **Types**: Use type hints for all function parameters and return values
- **Naming**:
  - Classes: `PascalCase`
  - Functions/methods: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`
  - Variables: `snake_case`
- **Error Handling**: Use specific exceptions, avoid bare `except`
- **Dependencies**: Project uses `smolagents`, `selenium`, `helium`, and `pillow`

## Package Management
- Project uses `uv` for dependency management
- Dependencies tracked in `uv.lock` file
- Use `uv sync` to install exact dependencies from lock file

## Repository Structure
- Web automation tools for autonomous agents
- Uses Python 3.12+