# Design Document: Chromie


## Introduction

### Purpose of *Chromie*

**Chromie** is a command-line tool (CLI) designed to facilitate importing and exporting data from and to a **Chroma** vector database.

The project is composed of two main parts:

- **chromio**:
  A **Python** library that contains all the business logic for interacting with **Chroma**.
  It is reusable and can be integrated into other projects.

- **chromie**:
  The CLI application that consumes the **chromio** library to expose its functionality to the end user through commands.

### Abbreviations

The following abbreviations will be used in the code:

Abbreviations | Description
:--: | :--:
cmd | command
coll | collection
db | database
dir | directory
doc | document
ie | import/export
meta | metadata
rec | record
rpt | report


## General Architecture

### Separation of Concerns

**Chromie**'s architecture is based on a clear separation between the business logic and the user interface.

- **chromio** Library:

  - Has no knowledge of the CLI.

  - Manages the connection to **Chroma**.

  - Contains the logic for reading, writing, filtering, and transforming data.

  - Defines the data structures for operation reports.

  - It is asynchronous, using **asyncio**.

- **chromie** Application:

  - Is the entry point for the user.

  - Uses **argparse** to define and parse commands and arguments.

  - Orchestrates calls to the **chromio** library to execute the requested actions.

  - Is responsible for presenting results and reports to the user in the console.

### High-Level Component Diagram

```mermaid
---
title: Component Diagram
config:
---

graph LR
  chromie@{ icon: "fa:file", label: "chromie" }
  chromio@{ icon: "fa:folder", label: "chromio" }
  chromadb@{ icon: "fa:folder", label: "chromadb" }
  dbms@{ shape: "lin-cyl", label: "DBMS" }

  chromie --> chromio  --> chromadb --> dbms
```


## *chromio* Library

### *Chroma* Connectivity

The connection is managed by two main components:

- **`uri`**:
  Connection URI parser, returns ***`ChromioUri`*** instances that describe the URI and facilitate access to its components.

- **`client`**:
  Client for a **Chroma** instance based on a ***`ChromioUri`*** and additional information if necessary.

### Import/Export Engine (`ie`)

This is the core of the library and contains the logic for moving data.

```mermaid
classDiagram
  direction TB

  class CollIEBase {
    <<abstract>>
    batch_size: int
    fields: Field[]
  }

  %%%%%%%%%%%%
  %% export %%
  %%%%%%%%%%%%
  class CollReader {
    read(coll, fields, batch_size, limit, metafilter)
  }

  class CollExporter {
    export_coll(coll, file, limit, metafilter) CollExportRpt
  }

  CollIEBase <|-- CollExporter
  CollExporter ..> CollReader

  %%%%%%%%%%%%
  %% import %%
  %%%%%%%%%%%%
  class CollWriter {
    write(records, coll, fields, limit, batch_size)
  }

  class CollImporter {
    import_coll(coll, file, limit) CollImportRpt
  }

  CollIEBase <|-- CollImporter
  CollImporter ..> CollWriter
```


## *chromie* CLI

### Entry Point (*app.py*)

Main program file.

### Command Structure (*cmds/*)

Each command is represented and implemented by a module in this directory.
Each of them inherits from or specializes the ***`Cmd`*** class defined in ***`chromio.tools`***.

```mermaid
classDiagram
  direction TB

  class Cmd {
    <<abstract>>
  }
  
  Cmd <|-- ExpCmd
  Cmd <|-- ImpCmd
  Cmd <|-- LsCmd
  Cmd <|-- UriCmd
  Cmd <|-- PingCmd
```