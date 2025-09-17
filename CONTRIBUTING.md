# Contributing to DeputyDev Auth

Thanks for your interest in improving DeputyDev Auth! This guide explains the project layout, local development workflows, code style, and how to submit changes.

If you’re new to this codebase, start with the README and in-code docstrings. Any previously separate docs pages are no longer required.


## Project layout (quick tour)

- app/ — Application source
  - main/ — HTTP routes and services
  - listeners.py — Sanic lifecycle listeners
  - service.py — App bootstrap and entrypoint
- config_template.json, config.json — Application configuration (see README)
- pyproject.toml — Project metadata, dependencies, Python version
- ruff.toml — Lint/format rules
- .pre-commit-config.yaml — Hooks (Ruff, uv-lock)
- uv.lock — Dependency lockfile
- README.md — Overview, prerequisites, and local setup
- CODE_OF_CONDUCT.md — Community standards


## Prerequisites and local setup

To avoid duplication, prerequisites (Python version, uv) and setup steps live in README.md. Follow the README for installing dependencies, enabling pre-commit, and running local checks.

Key versions (from pyproject.toml):
- Python: >= 3.12, < 3.13
- Package manager: uv (uv.lock is authoritative)


## Install and build

See README.md for the authoritative setup and build instructions (uv sync, pre-commit install, Ruff commands). This document focuses on contribution workflows and standards.


## Code style and quality

Type hints and style
- Type hints are required for function parameters and return types (public and private). Annotate *args/**kwargs as needed.
- Keep modules cohesive and small.
- Avoid top-level side effects on import; prefer explicit functions/classes.

Ruff (lint and format)
- Format: ruff format .
- Lint: ruff check .
- Config: ruff.toml (line-length 120, import ordering, PEP8 naming, complexity checks, no print statements, prefer pathlib, async best practices, and ANN* type-hint rules)

Pre-commit
- Install: pre-commit install
- Run all hooks: pre-commit run --all-files


## Submitting changes

1) Fork-based workflow (default; non-maintainers)
- Non-maintainers cannot create branches on the upstream repository.
- Fork this repository to your GitHub account.
- In your fork, create a branch using the same conventions: feat/…, fix/…, chore/…, docs/…
- Push to your fork and open a Pull Request against the upstream default branch (usually main). If unsure, target main.
- Enable "Allow edits by maintainers" on the PR.

2) Maintainers-only workflow (optional)
- Maintainers may create branches directly in the upstream repository.
- Branch naming: feat/…, fix/…, chore/…, docs/…

3) Ensure quality gates pass
- Local lint/format pass (ruff format, ruff check)
- Pre-commit hooks pass
- Update README.md if you introduce user-visible changes or configuration
- Add tests or usage notes for behavioral changes

4) Commit messages
- Use Conventional Commits with a scope when possible: feat(auth): ..., fix(main): ...
- Common types: feat, fix, chore, docs, refactor, test, perf, build, ci, revert
- Keep messages concise and reference issues when applicable

5) Open a Pull Request
- Describe the motivation, what changed, and how you validated it
- Link related issues
- Avoid bumping the version; maintainers handle releases


## Versioning and release notes

- Project version is defined in pyproject.toml.
- Coordinate version bumps with maintainers; do not change the version in PRs unless asked.


## Security and privacy

- Do not commit secrets or tokens. Use local environment configuration (config.json) and secret stores.
- Be mindful of logs; avoid including sensitive data in logs.


## Code of Conduct

By participating, you agree to abide by our Code of Conduct. See CODE_OF_CONDUCT.md at the repository root.


## Troubleshooting

- Python version errors: Ensure your Python matches the range in pyproject.toml (>=3.12, < 3.13).
- Missing tools: Ensure uv, pre-commit, and ruff are installed and available.
- Lockfile updates: If dependencies change, run uv lock (or rely on the uv-lock pre-commit hook) and commit uv.lock.
- Lint issues: Run ruff format . then ruff check . to see remaining violations.


## Questions?

Open an issue or start a discussion in the repository. Thanks again for contributing to DeputyDev Auth!