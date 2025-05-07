set quiet

# Default target, just listing available recipes
all:
   @just --list

# Fix linting violations and format code using ruff
ruff-fix:
    uvx ruff check --fix-only
    uvx ruff format

# Check for linting errors using ruff
ruff-check:
    uvx ruff check

# Run mypy to check for type errors
mypy:
    uv run --group types mypy --install-types --non-interactive app.py