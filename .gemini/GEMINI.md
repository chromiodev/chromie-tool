# Guide for the AI Assistant (Gemini)

This document provides the essential technical context for the AI assistant to collaborate effectively on the **Chromie** project.


## Project Overview

**Chromie** is a command-line interface (CLI) tool to facilitate importing and exporting data from and to a **Chroma** vector database.

The project is designed with a clear separation of responsibilities:

- **chromie/**:
  Contains the CLI application that the end-user runs.
  It is responsible for parsing command-line arguments and orchestrating operations.
  It uses the **chromio** library.

- **chromio/**:
  Contains the main library with all the business logic.
  It can be used independently in other projects.
  It is responsible for the interaction with **Chroma**, the import/export logic, handling URIs, etc.


## Technology Stack

- **Language**: Python 3.13+

- **Dependency and Environment Manager**: Poetry

- **CLI Framework**: parseargs

- **Formatting and Linting**: Ruff

- **Static Type Checking**: Pyright

- **Automated Testing**: pytest

- **Main Database**: Chroma


## Project Structure

```
.
├── chromie/         # CLI application (entry points and commands)
│   ├── app.py       # Main CLI entry point
│   └── cmds/        # Modules for each command (e.g., list, exp)
│
├── chromio/         # Main library with business logic
│   ├── client/      # Logic for creating and managing Chroma clients
│   ├── ie/          # Import/Export logic
│   └── uri/         # Utilities for parsing Chroma connection URIs
│
├── tests/
│   ├── functional/  # End-to-end functional tests for the CLI
│   └── unit/        # Unit tests for the chromio library
│
├── .gemini/         # Context and guides for the AI assistant
├── pyproject.toml   # Project definition, dependencies, and tool configuration
└── ...
```


## Contribution Workflow

01. **Create a branch**:
    Start from **main** and create a new descriptive branch.

    ```bash
    git checkout -b developer/feat/feature-name
    ```

02. **Implement the changes**:
    Make the necessary code modifications.

03. **Add or update tests**:
    Ensure that the changes are covered by unit, integration, or functional tests in the **tests/** directory.

04.  **Verify code quality**:
    Before committing, run the quality tools.

    ```bash
    ruff format .
    ruff check .
    pyright
    ```

05. **Run all tests**: Confirm that your changes have not broken any existing functionality.

    ```bash
    pytest
    ```

06. **Make the commit**:
    Write a clear and concise commit message.


## Style guide

The project has a style guide that must be followed for all contributions.
This is available in the file **docs/styleguide.md**.
