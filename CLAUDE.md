# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Synchronous, fully-typed Python wrapper for the Clash Royale API. Built on httpx + Pydantic v2. Requires Python >=3.12.

## Commands

```bash
uv sync --dev                        # Install dependencies
uv run pytest                        # Run all tests
uv run pytest tests/resources/test_clans.py  # Run specific test file
uv run pytest -k test_get_player     # Run specific test
uv run ruff check .                  # Lint
uv run ruff format .                 # Format
uv run ty check                      # Type check
uv run pre-commit run -a             # Run all pre-commit hooks
```

## Architecture

**Client** (`client.py`): Subclasses `httpx.Client`. Provides resource accessors (`client.players`, `client.clans`, etc.). Automatically converts snake_case params to camelCase for the API.

**Resources** (`resources/`): Each API domain (Players, Clans, Cards, Locations, Tournaments, GlobalTournaments, Leaderboards) is a `Resource` subclass. Tags are normalized (uppercased, `#` prefixed) and URL-encoded. List methods return `PaginatedList[T]`.

**Models** (`models/`): Pydantic v2 models inheriting `CRBaseModel` (configured with `populate_by_name=True`, `extra="ignore"`). Fields use `alias=` for camelCase API mapping. Custom `ISO8601DateTime` type parses the API's datetime format.

**PaginatedList** (`pagination.py`): Generic lazy-loading container with cursor-based pagination. `limit` controls total results; `page_size` controls per-request count. Supports slicing, indexing, iteration.

**Exceptions** (`exceptions.py`): `ClashRoyaleHTTPError` with subclasses for 400, 403, 404, 429, 5xx. `InvalidAPIKeyError` raised by `CRAuth` on empty key.

## Testing

Tests use `@pytest.mark.vcr()` with pre-recorded HTTP cassettes (no real API calls). Cassettes live in `tests/cassettes/` and `tests/resources/cassettes/`. VCR config is in `tests/conftest.py` — matches on method, scheme, host, port, path, query; filters out Authorization header.

## Commit Convention

Conventional commits: `<type>(<scope>): <description>` — imperative, lowercase, no period, max 100 chars. Use `!` before `:` for breaking changes.

### Types

- **feat**: Add, adjust or remove a feature (API/UI)
- **fix**: Fix a bug from a preceded feat commit
- **refactor**: Restructure code without altering behavior
- **perf**: Improve performance (special type of refactor)
- **style**: Code style (formatting, whitespace, missing semi-colons)
- **test**: Add missing tests or correct existing ones
- **docs**: Documentation changes only
- **build**: Build components (dependencies, project version, build tools)
- **ops**: Infrastructure, deployment, CI/CD, monitoring, backups
- **chore**: Tasks like initial commit, modifying .gitignore
