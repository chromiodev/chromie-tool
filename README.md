# chromie-tool

**Chroma** ([https://trychroma.com](https://trychroma.com)) import/export tool.


## Install

```bash
# install
pip install chromie-tool

# check chromie tool
which chromie
```


## Commands

### Help

```bash
# chromie help
chromie -h

# exp command help
chromie exp -h
```

### Download prepared datasets

Prepared datasets: [https://github.com/chromiodev/datasets](https://github.com/chromiodev/datasets).

```bash
chromie dl -l es eurostat/prc_hicp_manr
```

### Export

```bash
chromie exp server://localhost:8000/tenant/db/collection file.json
```

### Check an export file

```bash
chromie check prc_hicp_manr-es.json
```

### Import

```bash
# import all the content of movies.json
chromie imp movies.json server://localhost:8000/tenant/db/collection

# import all the content of movies.json, skipping the cert and rating metadata
chromie imp movies.json -M cert,rating server://localhost:8000/tenant/db/collection

# import all the content of movies.json, setting the cert and dir metadata
# to the specified values
chromie imp movies.json -m cert:C,dir:D server://localhost:8000/tenant/db/collection
```

### Copy

```bash
chromie cp server://///coll1 server://///coll2
```

### Listing the database collections

```bash
# only names
chromie ls server:////

# names and counts
chromie ls -c server:////
```

### Metadata filters

The **`--metafilter`** or **`-f`** options allow to select records from metadata in the **`cp`** and **`exp`** commands.
Format:

```
predicate
predicate and predicate
predicate or predicate
```

Examples:

```
-f "dir='Quentin Tarantino'"
-f "dir='Quentin Tarantino' or dir='Alfred Hitchcock'"
-f "dir in ['Quentin Tarantino', 'Alfred Hitchcock']"
```

Predicates:

```
field     # similar to: field == true
not field # similar to: field != true
field = literal_scalar
field == literal_scalar
field != literal_scalar
field < literal_scalar
field <= literal_scalar
field > literal_scalar
field >= literal_scalar
field in [literal_scalar, literal_scalar, ...]
field not in [literal_scalar, literal_scalar, ...]
field between literal_num|literal_text and literal_num|literal_text
field not between literal_num|literal_text and literal_num|literal_text
```

Literals:

- Literal text: *'A text'*.

- Literal number: *1234*.

- Literal boolean: *true* or *false*.


## URIs

### Server URI

Format:

```
server://host:port/tenant/database
server://host:port/tenant/database/collection
```

When a segment must take its value from the default value or an environment variable, this must be left blank.
Examples:

```
server://///
server:///tenant/db
```

Environment variables we can use for settings segments in server URIs:

- **`CHROMA_HOST`**

- **`CHROMA_PORT`**

- **`CHROMA_TENANT`**

- **`CHROMA_DATABASE`**

The default values in server URIs, when blank segments and environment variable unset, are these set in the **chromadb** package.
Right now:

- **Host**: ***localhost***

- **Port**: ***8000***

- **Tenant**: ***default_tenant***

- **Database**: ***default_database***

### Chroma Cloud URI

Format:

```
cloud:///tenant/db
cloud:///tenant/db/collection
```

Similar to the ***server*** schema but, with the ***cloud*** schema, the environment variables we can use are the following:

- **`CHROMA_TENANT`**

- **`CHROMA_DATABASE`**

Default values:

- **host:port** segment is always ***api.trychroma.com:8000***.

- Tenant and database don't have default values, these must be set explicitly or with environment variables.

### Checking and decomposing URIs

With **`chromie uri`**, we check and decompose a URI.
Examples:

```
$ chromie uri server:////
Schema: server
Host: localhost
Port: 8000
Tenant: default_tenant
Database: default_database

$ CHROMA_PORT=8888 chromie uri server:////
Schema: server
Host: localhost
Port: 8888
Tenant: default_tenant
Database: default_database

$ CHROMA_DATABASE=testdb chromie uri server://me//
Schema: server
Host: me
Port: 8000
Tenant: default_tenant
Database: testdb
```

### Pinging database instance and/or collection

Examples:

```
# database instance
chromie ping server:////

# database collection
chromie ping server://///movies
chromie ping cloud://///movies
```


## API key

When API key needed, **`--key`** or **`-k`** must be set.
We can use the **`CHROMA_API_KEY`** environment variable too.
