# Style Guide


## Introduction

This document establishes the coding conventions and style guides to be followed.
The goal is to maintain clean, readable, and consistent code throughout the project.
Adherence to these rules is mandatory for all contributors.


## Code Quality Tools

Consistency is primarily achieved through automated tools.
Before committing any changes, you must ensure that the code is error-free using the following tools:

- **`Ruff`**: For code formatting and linting.

- **`Pyright`**: For static type analysis and checking.

The configuration for these tools can be found in the **.ruff.toml**, **ruff.format.toml**, and **pyrightconfig.json** files.


## Code Formatting

- **Automatic formatter**: All **Python** code must be formatted using the **`ruff format`** command.

- **Line length**: A maximum of 90 characters per line is set.

- **Indentation**: Use 2 spaces per indentation level.


## Naming Conventions

- **Classes**: Use **PascalCase** (e.g., *`ChromieArgParser`*, *`CollExporter`*).

- **Functions, Methods, and Variables**: Use `snake_case` (e.g., `parse_args_and_run()`, `file_path()`).

- **"Private" Modules and Members**: Prefix modules, functions, or variables not intended for use outside their direct scope with an underscore (`_`) (e.g., `_client.py`).

- **Constants**: Use `UPPER_SNAKE_CASE` for module-level constants (e.g., `DEFAULT_TIMEOUT = 60`).


## Static Typing

- **Mandatory**: All new code must include type hints.

- **Clarity**: Use the most specific types possible (e.g., `list[str]` instead of `list`).
  For unions, the `int | None` format will be used instead of `Optional[int]`.

- **Verification**: The code must pass **pyright** verification without errors.


## Docstrings

- **Format**:
  Docstrings should follow a style similar to **Google's**.
  They must be clear and concise.

- **Structure**:

    01. A one-line summary describing the purpose of the function or class.

    02. A more detailed paragraph if necessary.

    03. An **Args:** section to describe the arguments.

    04. A **Returns:** section to describe the return value.

    05. A **Raises:** section to describe the exceptions raised.

- **Example**:

  ```python
    async def export(
    self,
    coll: AsyncCollection,
    file: Path,
    limit: int | None = None,
    metafilter: dict | None = None,
  ) -> CollExportRpt:
    """Exports a collection to a file.

    Args:
      coll: Collection to export.
      file: File path where to save the export.
      limit: Maximum number of records to export.
      metafilter: Filter by metadata.

    Returns:
      An export report.
    """
  ```


## Testing

- **Framework**:
  **pytest** is used for *all* automated tests.

- **Location**:

    - **tests/unit**: For unit tests.

    - **tests/integration**: For integration tests.

    - **tests/functional**: For functional tests.

- **Test Naming**:
  Test file names must follow the **\*_test.py** pattern.
  To avoid naming conflicts, integration test files must be prefixed with **itg_** and functional ones with **fn_**.
  No special affix needs to be applied to unit tests.
  
  Test functions must start with **test_**.

- **Test Structure**: Follow the **AAA(C)** (*arrange, act, assessment, cleanup*) pattern.
  Each block should be preceded by a comment that identifies it.
  Example:

  ```python
  async def test_server_client(mocker: MockerFixture) -> None:
    """Check that client() returns an asynchronous client."""

    # (1) arrange
    AsyncHttpClient = mocker.patch(
      "chromio.client._client.AsyncHttpClient", new_callable=mocker.AsyncMock
    )

    # (2) act
    out = await client(ChromioUri.server())

    # (3) assessment
    assert isinstance(out, AsyncMockType)
    assert AsyncHttpClient.await_count == 1
  ```

- **Fixtures**:
  The use of **pytest** *fixtures* is recommended for the *arrange* and *cleanup* sections.

- **Mocks**:
  For creating test doubles (*mocks*, *stubs*, etc.), the **pytest-mock** component must be used.
  The direct use of **`unittest.mock`** is not allowed.

- **Test Data**:
  Synthetic data will be generated with the **Faker** plugin integrated into **pytest**.

- **Custom Markers**:
  
  - ***`pytest.mark.readonly`*** to identify read-only integration and functional tests.
    Tests that do not have this mark are considered R/W.

  - ***`pytest.mark.attr(id="FT-component-number")`*** to link a functional test with its identifier in the specification document.


## Imports

- **Order**: Imports should be grouped in the following order, separated by a blank line:

  01. **Python** standard libraries (e.g., ***`asyncio`***, ***`json`***, etc.).

  02. Third-party libraries (e.g., ***`pytest`***, ***`chromadb`***...).

  03. Application modules (***`chromie`***, ***`chromio`***).

- **Style**:
  Direct imports (***`from module import name`***) are recommended over importing the entire module (***`import module`***).


## Git Commit Messages

To maintain a clean and navigable commit history, it is suggested to follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
type(component or scope): description
```