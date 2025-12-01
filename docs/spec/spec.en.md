# *Chromie* project specification


## Introduction

**Chroma** is establishing itself as a reference vector database management system due to its simplicity and power.
However, a gap has been identified in its data import and export tools.
The current **Chroma** command-line interface (CLI) does not allow storing data in portable files, limiting its use to migration between instances.

This document details the design and requirements for the **Chromie** (*Chroma Import/Export*) project, an open-source CLI tool designed to address this need.
Its purpose is to provide an intuitive interface for importing and exporting records from **Chroma** collections to standardized **JSON** files, for local and remote instances, as well as **Chroma Cloud**.

The purpose of this document is to serve as a central reference point for understanding the project, its scope, and its requirements.


## Project vision

A command-line application designed to import and export **Chroma** collections to a standard **JSON** file format, facilitating data portability and backup.

### Audience

- Developers

- DBAs

- MLOps

### License

The project is released under the **GNU General Public License v3.0** (**GPLv3**), thus ensuring that any derivative work remains open-source software (**OSS**).


## Functional requirements

The application exposes its functionality through a command-line interface (CLI) that allows users to interact with **Chroma** databases.

### Use cases

[use-cases.md](use-cases.en.md)

### Supported environment variables

The following environment variables are used to configure the database connection:

Variable | Description
:--: | :--
CHROMA_HOST | Server to connect to.
CHROMA_PORT | Server port to connect to.
CHROMA_API_KEY | API key to use with Chroma Cloud.
CHROMA_TENANT | Database tenant identifier.
CHROMA_DATABASE | Database name.

### Data schema

The import and export file format adheres to the schema, written with **JSON Schema**, available in the [schema.json](schema.json) file.

### Connection string format

The URI connection strings are defined as follows:

Type | URI
:--: | :--
Local | path:///path/to/persistent/directory
Server | server://name:port/tenant/db/collection
Chroma Cloud | cloud:///tenant/db/collection


## Non-functional requirements

These requirements establish the project's quality attributes, constraints, and technical dependencies:

Requirement | Description
:--: | :--
IDE | VS Code
Modeling | UML (with Mermaid)
Platform | Python 3.14+
Concurrency | asyncio
Operating systems | Linux, Windows, macOS
Package management | Poetry
Linter | Ruff
Formatting | Ruff
Type checking | Pyright
Testing | pytest
Coverage | 100% with pytest-cov
Documentation of this document | Spanish, English
CI/CD | GitHub Actions
Chroma | chromadb
Parser generator | ANTLR4


## Project management

To maintain a healthy project and foster an active community, the following management guidelines have been defined.

### Roles

- **Maintainer**: Role assumed by the initial development team.
  They are responsible for the long-term direction of the project.
  A maintainer reviews pull requests, approves code, manages issue triage, and is the main contact for the community.

- **Contributor**: Anyone who submits a contribution to the project, whether it's a bug report, a code fix, or a documentation improvement.

- **Core Contributor**: A contributor who has demonstrated consistent commitment and has made significant, high-quality contributions.
  They may be granted additional permissions to help with code review or triage management.

### *GitHub* labels

**GitHub** labels will be used to classify and organize issues and pull requests.
This will make it easier for both existing and new contributors to find and track tasks.
These will be:

- **Status**: *pending triage*, *in progress*, *on hold*, *duplicate*.

- **Type**: *bug*, *feature* (for new functionalities), *doc* (for documentation improvements).

- **Priority**: *p:low*, *p:medium*, *p:high*, *p:critical*.

- **Effort**: *s:xs*, *s:s*, *s:m*, *s:l*, *s:xl*.

### Issue acceptance process

A clear process will be followed for accepting issues to optimize the workflow:

01. **Review/Triage**: A **maintainer** will review and validate new issues.
    This consists of:

    - **Validate**: Check that the information is clear and complete.
      If it's a *bug*, verify that it can be reproduced.
      If not, the author will be asked for more information.

    - **Identify duplicates**: Check if the problem has already been reported in another issue.
      If so, the new issue is closed (marked as *duplicate*) and linked to the original one.

    - **Clarify**: Act as the main point of contact to clarify doubts or request additional information from the author before the issue is assigned.

02. **Labeling**: Once validated, a **maintainer** will apply the appropriate labels to categorize the issue.
    The goal is for any contributor to understand the nature, priority, and difficulty of the task at a glance.

03. **Assignment**: After labeling, the issue is ready to be addressed.
    A **maintainer** will assign it to an interested contributor or to themselves, kicking off its implementation.

This process ensures that contributions are efficient and that contributors always know the status of tasks.


## Process for adding a new command to *chromie*

The process for adding a new command to **chromie** is described below:

01. Add the corresponding use cases to the [use-cases.en.md](use-cases.en.md) document.

02. Modify the [design.en.md](design.en.md) design document.

03. Modify the [schema.json](schema.json) schema document if necessary.

04. Add integration tests if necessary to [tests/integration.en.md](tests/integration.en.md).

05. Add functional tests to [tests/functional.en.md](tests/functional.en.md).


## *Gemini* and *Gemini Code Assist*

This project uses **Gemini** and **Gemini Code Assist** to support its development and the translation of documents in the **docs/spec/** directory into different languages.
The specific configuration for **Gemini Code Assist** is located in the project's **.gemini** directory and is a good starting point, along with this and other documents, for new contributors.
Configuration can also be found in **vscode/settings.json**.


## Other documents

- **Style guide**, [../styleguide.en.md](../styleguide.en.md).

- **Design document: Chromie**, [design.en.md](design.en.md).

- **Integration tests**, [tests/integration.en.md](tests/integration.en.md).

- **Functional tests**, [tests/functional.en.md](tests/functional.en.md).
