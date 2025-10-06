# Functional tests: chromie


## Introduction

The purpose of this document is to define and describe the functional test cases for the **chromie** command-line application.
The idea is to ensure a structured approach, focusing on the main functionalities of the tool.
It serves as a guide for the execution, validation, and documentation of the tests.

The tests are designed using a **black-box** approach, validating the observable behavior of the application (inputs and outputs) without knowledge of its internal structure.


## Scope

The main functionalities of **chromie** will be validated through its following main commands:

- **`chromie ls`**: Listing collections.

- **`chromie exp`**: Exporting data from a collection.

- **`chromie imp`**: Importing data to a collection.

- **`chromie cp`**: Copying data from one collection to another.


## Test environment

All tests will be executed in a controlled environment with the following configuration:

Dependency | Type | Description
:--: | :--: | :--
Hardware | Internal | Machine with at least 2GB of RAM
Operating system | Internal | Ubuntu 24.04
Python | Internal | 3.13
Testing framework | Internal | pytest 8.4
Chroma | Internal | Docker chromadb/chroma

The tests will be located in the **tests/functional** directory of the project.
Each test file must have the prefix **fn_** and the suffix **_test.py**, for example, *fn_exp_test.py*.


## Test cases

A test case is considered **successful** if all its expected output conditions are met.
It is considered **failed** if one or more of these conditions are not met.

### Listing collections (*LS*)

```mermaid
---
title: Test case diagram (listing collections)
config:
---

graph BT
  %% use cases
  listColls@{ shape: "rounded", label: "List collections" }

  subgraph "Test cases"
    listCollNames@{ shape: "rounded", label: "#lt;#lt;testcase>><br>FN-LS-01: Listing names" }
    listCollNamesAndCount@{ shape: "rounded", label: "#lt;#lt;testcase>><br>FN-LS-02: Listing names and record counts" }
    listOnUnknownServer@{ shape: "rounded", label: "#lt;#lt;testcase>><br>FN-LS-03: Attempt to list from an inaccessible DB" }
  end


  listCollNames -.-> listColls
  listCollNamesAndCount -.-> listColls
  listOnUnknownServer -.-> listColls
```

#### Listing names (*FN-LS-01*)

- **Description**:
  Checks that the **`chromie ls`** command lists the names of the collections present in an existing database.

- **Type**:
  Read.

- **Preconditions**:
  
  - The database contains at least two collections.

- **Postconditions**:
  The system state is not altered.

- **Expected output**:

  - **Exit code**: 0.

  - **Standard output**: The names of all existing collections are displayed, one per line.

#### Listing names and record counts (*FN-LS-02*)

- **Description**:
  Checks that the **`chromie ls --count`** command lists the names and the number of records for each collection.

- **Type**:
  Read.

- **Preconditions**:

  - The database contains at least two collections with a variable number of records.

- **Postconditions**:
  The system state is not altered.

- **Expected output**:

  - **Exit code**: 0.

  - **Standard output**: A table is displayed with the collection names and their corresponding record counts.

#### Attempt to list from an inaccessible database (*FN-LS-03*)

- **Description**:
  Checks that **`chromie ls`** shows an error when it cannot access the database.

- **Type**:
  Read.

- **Preconditions**:
  None.

- **Postconditions**:
  The system state is not altered.

- **Expected output**:

  - **Exit code**: 1.

  - **Error output**: An error message is displayed informing about the inability to connect to the database.

### Exporting data (*EXP*)

```mermaid
---
title: Test case diagram (exporting data)
config:
---

graph BT
  %% use cases
  exportColl@{ shape: "rounded", label: "Export collection" }

  subgraph "Test cases"
    exportExistingColl@{ shape: "rounded", label: "#lt;#lt;testcase>><br>FN-EXP-01: Export existing collection" }
    exportNonExistingColl@{ shape: "rounded", label: "#lt;#lt;testcase>><br>FN-EXP-02: Attempt to export non-existent collection" }
  end

  exportExistingColl -.-> exportColl
  exportNonExistingColl -.-> exportColl
```

#### Exporting an existing collection (*FN-EXP-01*)

- **Description**:
  Checks that the **`chromie exp`** command correctly exports the records of an existing collection to a file.

- **Type**:
  Read.

- **Preconditions**:
  
  - The test collection exists and contains records.

- **Postconditions**:

  - A file is generated in **JSON** format.

  - The file contains the same number of items as records in the collection.

- **Expected output**:

  - **Exit code**: 0.

  - **Standard output**: An operation report is displayed.

#### Attempt to export a non-existent collection (*FN-EXP-02*)

- **Description**:
  Checks that the **`chromie exp`** command shows an error when trying to export a non-existent collection.

- **Type**:
  Read.

- **Preconditions**:
  The specified collection does not exist in the database.

- **Postconditions**:
  The system state is not altered.

- **Expected output**:

  - **Exit code**: 1.
  
  - **Error output**: Error message indicating that the collection does not exist.

### Importing data (*IMP*)

```mermaid
---
title: Test case diagram (importing collections)
config:
---

graph BT
  %% use cases
  importColl@{ shape: "rounded", label: "Import collection" }

  subgraph "Test cases"
    importIntoEmptyColl@{ shape: "rounded", label: "#lt;#lt;testcase>><br>FN-IMP-01: Import into an empty collection" }
    importIntoNonEmptyColl@{ shape: "rounded", label: "#lt;#lt;testcase>><br>FN-IMP-02: Import into a non-empty collection" }
    importIntoNonExistingColl@{ shape: "rounded", label: "#lt;#lt;testcase><br>FN-IMP-03: Import into a non-existent collection" }
    importIntoUnknownServer@{ shape: "rounded", label: "#lt;#lt;testcase>><br>FN-IMP-04: Attempt to import into an inaccessible database" }
  end

  importIntoEmptyColl -.-> importColl
  importIntoNonEmptyColl -.-> importColl
  importIntoNonExistingColl -.-> importColl
  importIntoUnknownServer -.-> importColl
```

#### Importing into an empty collection (*FN-IMP-01*)

- **Description**:
  Checks that the **`chromie imp`** command correctly imports records from a file into an existing empty collection.

- **Type**:
  R/W.

- **Preconditions**:

  - The input file is valid and contains a known number of records.

  - The destination collection exists and is empty.

- **Postconditions**:

  - The collection contains the same number of records as the input file.

- **Expected output**:

  - **Exit code**: 0.

  - **Standard output**: An operation report is displayed.

#### Importing into a non-empty collection (*FN-IMP-02*)

- **Description**:
  Checks that the **`chromie imp`** command inserts records into an existing non-empty collection.

- **Type**:
  R/W.

- **Preconditions**:

  - The input file is valid.

  - The destination collection exists and contains records.

- **Postconditions**:

  - The collection contains the initial data plus the new data.

- **Expected output**:

  - **Exit code**: 0.

  - **Standard output**: An operation report is displayed, indicating the number of processed records.

#### Attempt to import into an inaccessible database (*FN-IMP-03*)

- **Description**:
  Checks that **`chromie imp`** handles the error when the destination database is not accessible.

- **Type**:
  No R/W.

- **Preconditions**:

  - The input file is valid.

- **Postconditions**:
  The state of any database is not altered.

- **Expected output**:

  - **Exit code**: 1.

  - **Error output**: An error message is displayed informing about the inability to connect to the database.

### URI parser (*URI*)

```mermaid
---
title: Test case diagram (URI)
config:
---

graph BT
  %% use cases
  printUri@{ shape: "rounded", label: "Show URI segments" }

  subgraph "Test cases"
    printServerUri@{ shape: "rounded", label: "#lt;#lt;testcase>><br>FN-URI-01: Show segments of a server URI" }
    printCloudUri@{ shape: "rounded", label: "#lt;#lt;testcase>><br>FN-URI-02: Show segments of a cloud URI" }
    invalidCloudUri@{ shape: "rounded", label: "#lt;#lt;testcase>><br>FN-URI-03: Attempt with an invalid cloud URI" }
  end

  printServerUri -.-> printUri
  printCloudUri -.-> printUri
  invalidCloudUri -.-> printUri
```

#### Showing segments of a server URI (*FN-URI-01*)

- **Description**:
  Checks that **`chromie uri`** shows the segments of a server URI.

- **Type**:
  No R/W.

- **Preconditions**:
  
  - The **`CHROMA_PORT`** environment variable has been set to ***8008***.

- **Postconditions**:
  The state of any database is not altered.

- **Expected output**:

  - **Exit code**: 0.

  - **Standard output**: Shows the URI segments.

#### Showing segments of a cloud URI (*FN-URI-02*)

- **Description**:
  Checks that **`chromie uri`** shows the segments of a *cloud* URI.

- **Type**:
  No R/W.

- **Preconditions**:
  
  - The **`CHROMA_TENANT`** and **`CHROMA_DATABASE`** environment variables have non-default values.

- **Postconditions**:
  The state of any database is not altered.

- **Expected output**:

  - **Exit code**: 0.

  - **Standard output**: Shows the variable names with their respective values.

#### Attempt with an invalid cloud URI (*FN-URI-03*)

- **Description**:
  Checks that **`chromie uri`** shows an error when the URI does not have a tenant.

- **Type**:
  No R/W.

- **Preconditions**:
  
  - The **`CHROMA_TENANT`** and **`CHROMA_DATABASE`** environment variables are not defined.

- **Postconditions**:
  The state of any database is not altered.

- **Expected output**:

  - **Exit code**: 1.

  - **Error output**: Shows an error due to the missing tenant.

### URI check (*PING*)

```mermaid
---
title: Test case diagram (PING)
config:
---

graph BT
  %% use cases
  pingServer@{ shape: "rounded", label: "Check connection to instance" }

  subgraph "Test cases"
    pingReachableServer@{ shape: "rounded", label: "#lt;#lt;testcase>><br>FN-PING-01: Check connection to a reachable server" }
    pingReachableColl@{ shape: "rounded", label: "#lt;#lt;testcase>><br>FN-PING-02: Check connection to an existing collection" }
    pingUnreachableServer@{ shape: "rounded", label: "#lt;#lt;testcase>><br>FN-PING-03: Attempt to connect to an unreachable server" }
  end

  pingReachableServer -.-> pingServer
  pingReachableColl -.-> pingServer
  pingUnreachableServer -.-> pingServer
```

#### Checking connection to a reachable server (*FN-PING-01*)

- **Description**:
  Checks that **`chromie ping`** connects to a server and shows that everything went well.

- **Type**:
  No R/W.

- **Preconditions**:
  None.

- **Postconditions**:
  The state of any database is not altered.

- **Expected output**:

  - **Exit code**: 0.

  - **Standard output**: Shows that the communication was successful.

#### Checking connection to an existing collection (*FN-PING-02*)

- **Description**:
  Checks that **`chromie ping`** connects to a server and verifies the existence of a given collection, showing that everything went well.

- **Type**:
  No R/W.

- **Preconditions**:
  
  - The collection exists.

- **Postconditions**:
  The state of any database is not altered.

- **Expected output**:

  - **Exit code**: 0.

  - **Standard output**: Shows that the communication was successful.

#### Attempt to connect to an unreachable server (*FN-PING-03*)

- **Description**:
  Checks that **`chromie ping`** shows an error message when the server cannot be reached.

- **Type**:
  No R/W.

- **Preconditions**:
  None.

- **Postconditions**:
  The state of any database is not altered.

- **Expected output**:

  - **Exit code**: 1.

  - **Error output**: Shows an error message.

### Copying data (*CP*)

```mermaid
---
title: Test case diagram (copying collections)
config:
---

graph BT
  %% use cases
  copyColl@{ shape: "rounded", label: "Copy collection" }

  subgraph "Test cases"
    copyReachableColl@{ shape: "rounded", label: "#lt;#lt;testcase>><br>FN-CP-01: Copy a collection" }
    copyNonReachableColl@{ shape: "rounded", label: "#lt;#lt;testcase><br>FN-CP-02: Attempt to copy from an unreachable source collection" }
  end

  copyReachableColl -.-> copyColl
  copyNonReachableColl -.-> copyColl
```

#### Copying a collection (*FN-CP-01*)

- **Description**:
  Checks that the **`chromie cp`** command correctly copies records from one collection to another.

- **Type**:
  R/W.

- **Preconditions**:

  - The source collection exists and contains a known number of records.

  - The destination collection exists and is empty.

- **Postconditions**:

  - The destination collection contains the same number of records as the source one.

- **Expected output**:

  - **Exit code**: 0.

  - **Standard output**: An operation report is displayed.

#### Attempt to copy from an unreachable source collection (*FN-CP-02*)

- **Description**:
  Checks that the **`chromie cp`** command handles the error when the source collection is not reachable.

- **Type**:
  R/W.

- **Preconditions**:

  - The source collection does not exist.

- **Postconditions**:
  The state of any database is not altered.

- **Expected output**:

  - **Exit code**: 1.

  - **Error output**: An error message is displayed informing about the inability to connect to the source collection.