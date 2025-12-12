# Contributing to SemantIQ

## Development Setup
- Install Python 3.11+
- Create a virtual environment
- Install in editable mode: `python -m pip install -e .[all]`
- Run tests: `pytest -q`

## Branching & Commits
- Use short, descriptive branches: `feature/...`, `fix/...`, `docs/...`
- Prefer conventional commits: `feat:`, `fix:`, `docs:`, `test:`, `chore:`

## Coding Style
- Type hints required
- Lint with `ruff`; format with `black`
- Keep modules small, cohesive, and well-structured

## Testing
- Write unit tests for new features
- Ensure `pytest` passes locally before PR

## Pull Requests
- Include concise description
- Reference issues and motivations
- Keep PRs focused and reviewable
