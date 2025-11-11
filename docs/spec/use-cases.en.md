# Use cases: Chromie

## Actors

```mermaid
---
config:
---

graph BT
  user@{ icon: "fa:user", label: "User" }
  dba@{ icon: "fa:user", label: "DBA" }
  dev@{ icon: "fa:user", label: "Developer" }

  user
  dba -->|«generalize»| user
  dev -->|«generalize»| user
```

## Use cases

### Miscellaneous

```mermaid
---
config:
---

graph LR
  %%%%%%%%%%%%%
  %% actors %%
  %%%%%%%%%%%%%
  user@{ icon: "fa:user", label: "User" }

  %%%%%%%%%%
  %% UC %%
  %%%%%%%%%%
  printUriSegments@{ shape: "rounded", label: "Show URI segments<hr>
    «in» URI
    «out» URI segments
  " }

  pingInstance@{ shape: "rounded", label: "Check instance connection<hr>
    «in» URI
    «in» API key
    «out» OK or error
  " }

  %%%%%%%%%%%%%%%%
  %% relationships %%
  %%%%%%%%%%%%%%%%
  user --> printUriSegments
  user --> pingInstance
```

#### Show URI segments

- **User story**:
  As a *user*,
  I want to *analyze and know the segments of a URI*
  so that I can *know if I have written it correctly before using it*.

- **Priority**:
  High

- **Input**:

  - URI to analyze.

- **Output**:

  - Segments of the analyzed URI.

#### Check instance connection

- **User story**:
  As a *user*,
  I want to *check if I have access to an instance*
  so that I can *know if I can connect to it to export and/or import*.

- **Priority**:
  High

- **Input**:

  - URI of the instance to connect to.

  - API key if required for connection.

- **Output**:

  - Was the connection successful?

### Collections

```mermaid
---
config:
---

graph LR
  %%%%%%%%%%%%%
  %% actors %%
  %%%%%%%%%%%%%
  user@{ icon: "fa:user", label: "User" }

  %%%%%%%%%%
  %% UC %%
  %%%%%%%%%%
  listColls@{ shape: "rounded", label: "List collections<hr>
    «in» URI
    «in» API key
    «out» Collection names
  " }

  createColl@{ shape: "rounded", label: "Create a collection<hr>
    «in» URI
    «in» API key
  " }
  
  printCollConf@{ shape: "rounded", label: "Show collection info<hr>
    «in» URI
    «in» API key
  " }

  %%%%%%%%%%%%%%%%
  %% relationships %%
  %%%%%%%%%%%%%%%%
  user --> listColls
  user --> createColl
  user --> printCollConf
```
#### List available collections

- **User story**:
  As a *user*,
  I want to *know the available collections*,
  so that I can *know which collections I can export from or insert new records into*.

- **Priority**:
  High

- **Input**:

  - URI of the instance to access.

  - API key if required to open the connection.

  - Do we want to know the number of records it has?

- **Output**:

  - List with the names of the collections and their counters if requested.

#### Create a collection

- **User story**:
  As a *user*,
  I want to *create collections*,
  so that I can *facilitate the configuration of new collections to import into*.

- **Priority**:
  High

- **Input**:

  - URI of the instance to access.

  - API key if required to open the connection.

- **Output**:

  - Creation report.

#### Show collection info

- **User story**:
  As a *user*,
  I want to *know the information of a collection*,
  so that I can *know its current configuration*.

- **Priority**:
  High

- **Input**:

  - URI of the instance to access.

  - API key if required to open the connection.

- **Output**:

  - Collection info.

### Data export

```mermaid
---
config:
---

graph LR
  %%%%%%%%%%%%%
  %% actors %%
  %%%%%%%%%%%%%
  user@{ icon: "fa:user", label: "User" }

  %%%%%%%%%%
  %% UC %%
  %%%%%%%%%%
  exportColl@{ shape: "rounded", label: "Export collection<hr>
    «in» URI
    «in» API key
    «in» Collection name
    «in» Names of the fields to export
    «in» Read batch size
    «in» Path to the export file
    «out» Export report
  " }

  exportDb@{ shape: "rounded", label: "Export database<hr>
    «in» URI
    «in» API key
    «in» Names of the fields to export
    «in» Read batch size
    «in» Path to the export directory
    «in» Number of export tasks
    «out» Export report
  " }

  checkExportFile@{ shape: "rounded", label: "Validate export file schema<hr>
    «in» Path to the file to validate
  " }
  
  %%%%%%%%%%%%%%%%
  %% relationships %%
  %%%%%%%%%%%%%%%%
  user --> exportColl
  user --> exportDb -.->|«include»| exportColl
  user --> checkExportFile
```

#### Export collection

- **User story**:
  As a *user*,
  I want to *export the data from a collection*
  so that I can *import it into another collection, exchange it, or save it*.

- **Priority**:
  High

- **Input**:

  - Instance URI.

  - API key, if required, to connect to the instance.

  - Name of the collection to export.

  - Names of the fields to export.

  - Read batch size.

  - Path to the export file to be generated.

- **Output**:

  - Export report.

#### Export database

- **User story**:
  As a *user*,
  I want to *export the data from a database*
  so that I can *import it into another one, exchange it, or save it*.

- **Priority**:
  Low (can be implemented using *Export collection*)

- **Input**:

  - Instance URI.

  - API key, if required, to connect to the instance.

  - Names of the fields to export.

  - Read batch size.

  - Path to the export directory.

  - Number of concurrent export tasks.

- **Output**:

  - Export report.

#### Validate an export file's schema

- **User story**:
  As a *user*,
  I want to *validate the schema of an export file*
  so that I can *ensure that an explicitly generated one complies with the official schema*.

- **Priority**:
  High

- **Input**:

  - Path to the file to validate.

- **Output**:

  - OK or error.

### Data import

```mermaid
---
config:
---

graph LR
  user@{ icon: "fa:user", label: "User" }

  importColl@{ shape: "rounded", label: "Import collection<hr>
    «in» URI
    «in» API key
    «in» Name of the collection to import into
    «in» Names of the fields to import
    «in» Write batch size
    «in» Path to the export file to import
    «out» Import report
  " }

  user --> importColl
```

#### Import collection

- **User story**:
  As a *user*,
  I want to *import an export file*
  so that I can *incorporate its data into a collection*.

- **Priority**:
  High

- **Input**:

  - URI of the instance to work with.

  - API key if required for connection.

  - Name of the collection to import into.

  - Names of the fields to import.

  - Write batch size.

  - Path of the export file to import.

- **Output**:

  - Import report.

### Data copy

```mermaid
---
config:
---

graph LR
  user@{ icon: "fa:user", label: "User" }

  copyColl@{ shape: "rounded", label: "Copy collection<hr>
    «in» Source URI
    «in» Source API key
    «in» Destination URI
    «in» Destination API key
    «in» Collection to copy
    «in» Names of the fields to copy
    «in» Read/write batch size
    «out» Copy report
  " }

  user --> copyColl
```

#### Copy collection

- **User story**:
  As a *user*,
  I want to *make a copy of a collection in another instance*
  so that I can *move data between instances*.

- **Priority**:
  Medium

- **Input**:

  - URI of the source data instance.

  - Source API key if required.

  - URI of the destination data instance, which can be the same or a different instance.

  - Destination API key if required.

  - Name of the collection to copy.

  - Names of the fields to copy.

  - R/W batch size.

- **Output**:

  - Copy report.


### Data download

```mermaid
---
config:
---

graph LR
  user@{ icon: "fa:user", label: "User" }

  downloadDataset@{ shape: "rounded", label: "Download a dataset<hr>
    «in» Dataset identifier
    «in» Path to the destination data file
  "}

  user --> downloadDataset
```

#### Download a dataset

- **User story**:
  As a *user*,
  I want to *download a prepared dataset*
  so that I can *import it into a Chroma instance*.

- **Priority**:
  Medium

- **Input**:

  - Dataset identifier.

  - Path to the destination file where the data will be stored.