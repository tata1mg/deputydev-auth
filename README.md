# DeputyDev Auth

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

---

## Overview

**DeputyDev Auth** is a service that provides the backend functionality for DeputyDev Authentication. It integrates with various developer tools and AI services to offer intelligent assistance and automation.

## Tech Stack

- **Programming Language:** Python (>=3.12)
- **Framework:** FastAPI
- **Containerization:** Docker
- **Package Management:** [`uv`](https://github.com/astral-sh/uv) (via `uv.lock`)
- **Linting/Formatting:** Ruff

## Project Structure

```
/
├── app/                     # Main application code
│   ├── main/                # Main application logic, blueprints
│   ├── listeners.py         # Application event listeners
│   └── service.py           # Main service entry point
├── .gitignore               # Git ignore rules
├── .pre-commit-config.yaml  # Pre-commit hook configurations
├── config.json              # Application configuration
├── config_template.json     # Template for configuration
├── Dockerfile               # Docker build instructions
├── pyproject.toml           # Project metadata and dependencies (PEP 621)
├── README.md                # This file
└── uv.lock                  # uv lock file
```

---

## Setup and Installation

### Local Development Setup

1. **Prerequisites:**
    - Python >= 3.12, < 3.13
    - [`uv`](https://github.com/astral-sh/uv): `pip install uv`
    - Git

2. **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd deputydev-auth
    ```

3. **Install dependencies:**

    It is highly recommended to use a virtual environment:

    ```bash
    uv venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    uv sync
    ```

4. **Configure Environment Variables:**

    - Copy `config_template.json` to `config.json`.
    - Populate `config.json` with your credentials/configs

---

### Docker Setup

1. **Prerequisites:**
    - Docker installed and running.

2. **Build the Docker image:**

    ```bash
    docker build \
      -t deputydev-auth .
    ```

3. **Run the Docker container:**

    Mount the `config.json` so changes don't require a rebuild:

    ```bash
    docker run -d \
      -p <host_port>:<container_port> \
      -v "$(pwd)/config.json:/app/config.json" \
      --name deputydev-auth-container \
      deputydev-auth
    ```

    Replace `<host_port>` and `<container_port>` (e.g., `8000:8000`).

---

## Running the Application

### Locally

```bash
uv venv --python 3.12
source .venv/bin/activate
uv sync
python -m app.service
```

## Local checks

- pre-commit install
- pre-commit run --all-files
- ruff format .
- ruff check .

## Contributing

Please read CONTRIBUTING.md for contribution guidelines (project layout, code style, workflows, and PR process).

## Code of Conduct

By participating, you agree to follow our Code of Conduct (CODE_OF_CONDUCT.md).

