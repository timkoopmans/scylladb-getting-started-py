To effectively query data in ScyllaDB, you should understand its schema and how to perform basic operations like insert, read, update, and delete. To perform these basic operations, you will use CQL.

CQL
===
CQL, or Cassandra Query Language, is a query language for interacting with ScyllaDB, which is similar in syntax and usage to SQL for relational databases. It allows you to define, query, and modify data. CQL is designed to be simple and intuitive, making it easier for those familiar with SQL to transition to working with ScyllaDB.

## Using cqlsh
cqlsh is a command-line shell for interacting with ScyllaDB through CQL. It provides an interface to run CQL commands and scripts. cqlsh connects to a ScyllaDB node and allows you to execute CQL commands directly. This tool is essential for database management tasks and querying data.

In your [terminal](tab-0), copy and run the following code to connect to the node you started earlier in this track using cqlsh:

```run
docker exec -it node1 cqlsh
```

The output should look something like:

```
Connected to  at 172.21.0.2:9042
[cqlsh 6.0.23 | Scylla 6.1.1 | CQL spec 3.3.1 | Native protocol v4]
Use HELP for help.
cqlsh>
```

Schema
===
A schema represents the organization of data in ScyllaDB.

## Keyspace
A ScyllaDB keyspace contains tables and defines settings for replication. To create a keyspace, use the following syntax:

```run
CREATE KEYSPACE IF NOT EXISTS binance WITH replication = {
    'class': 'NetworkTopologyStrategy',
    'replication_factor': 1
};
```

Let’s break down the key concepts related to keyspace creation and replication in ScyllaDB.

### Keyspace Creation
To create a keyspace, you use the `CREATE KEYSPACE` command followed by a keyspace name. In the example above, `binance` is the name of the keyspace you want to create.

### Replication Strategy
Replication in ScyllaDB is the process of storing copies of data across multiple nodes to ensure fault tolerance and high availability. The replication strategy defines how data should be replicated across nodes in the cluster. In the example above, the replication strategy is set to `NetworkTopologyStrategy`.

This is a commonly used replication strategy in ScyllaDB, especially in production deployments. It allows you to specify the number of replicas for each datacenter separately, which provides fine-grained control over data distribution in a multi-datacenter environment. For example, if you have two datacenters, you can set different replication factors for each datacenter to handle data distribution and fault tolerance according to your specific requirements.

### Replication Factor
The replication factor specifies how many copies (or replicas) of each piece of data should be stored in the cluster. In the example above, the replication factor is set to 3. This means that each piece of data will be replicated to three different nodes in the cluster.

The replication factor determines how many copies of your data exist across the cluster and directly affects fault tolerance and read performance.

## Tables
Tables hold your data. Define them with specific column types and primary keys. Here’s how to create a table:

```run
CREATE TABLE IF NOT EXISTS binance.trades
(
    symbol    TEXT,
    counter   BIGINT,
    trade_id  BIGINT,
    timestamp BIGINT,
    price     DECIMAL,
    quantity  DECIMAL,
    PRIMARY KEY (symbol, counter)
);
```
Let’s break down the components of this `CREATE TABLE` statement:

### Keyspace
The `trades` table is created within the `binance` keyspace. This means that the `trades` table belongs to the `binance` keyspace, and all data stored in this table will be associated with that keyspace.

### Table
The name of the table being created is `trades`. This name should be unique within the keyspace.

### Columns
Columns in ScyllaDB are defined within a table and have a specified data type. In the above `trades` table, the columns are:

- **symbol**: This column is of type `TEXT` and stores the symbol of the trade.
- **counter**: This column is of type `BIGINT` and acts as a counter for the trades.
- **trade_id**: This column is of type `BIGINT` and stores the unique identifier for each trade.
- **timestamp**: This column is of type `BIGINT` and stores the timestamp of the trade.
- **price**: This column is of type `DECIMAL` and stores the price at which the trade was executed.
- **quantity**: This column is of type `DECIMAL` and stores the quantity of the trade.

### Primary Keys
The primary key can be made up of two parts: the partition key and optional clustering columns.
In this case, the primary key is `(symbol, counter)`, where `symbol` is the partition key and `counter` is the clustering key.

#### Clustering Key
The clustering key is used to sort the rows within the same partition. This can be useful for queries that need to retrieve rows in a specific order or range within the same partition. In the context of the `binance.trades` table, the clustering key counter can be useful for:
- Ensuring that trades for the same symbol are stored together and can be retrieved in the order of the counter.
- Efficiently querying trades for a specific symbol within a range of counter values.

If you need to frequently query trades for a specific symbol in a sorted order or within a specific range, the clustering key is very useful.

Writing and reading data
===
To write and read from the `binance.trades` table using CQL, you can use the following commands:

```run
INSERT INTO binance.trades (symbol, counter, trade_id, timestamp, price, quantity)
VALUES ('BTCUSD', 1, 1001, 1638316800, 57000.00, 0.5);
```
The `INSERT INTO` statement adds a new row to the trades table with the specified values.

> [!NOTE]
> Unlike in SQL, INSERT INTO does not check the prior existence of the row by default: the row is created if none existed before, and updated otherwise. This behavior can be changed by using ScyllaDB’s Lightweight Transaction IF NOT EXISTS or IF EXISTS clauses.

To read from the table use the following command:

```run
SELECT * FROM binance.trades WHERE symbol = 'BTCUSD';
```
The `SELECT` statement retrieves all rows from the trades table where the symbol is 'BTCUSD'.

Experiment yourself, reading and writing data manually using cqlsh before moving on to the next challenge, where you will learn how to hook up the demonstration application to the database.