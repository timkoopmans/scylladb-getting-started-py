To write and read from the `binance.trades` table in ScyllaDB using Python, you can use the scylla-driver library. Below is an example of how to do this.

Installing the driver
===
First, ensure you have the scylla-driver installed in your [terminal](tab-0):

```run
pip install scylla-driver
```

Next, open an interactive python shell in your [terminal](tab-0):

```run
python3
```

Using the driver
===
Using CQL code from our last challenge, we can now do something similar using python. The following code when run will
1. Connect to the ScyllaDB cluster.
2. Prepare an INSERT query to add data to the trades table.
3. Execute the query with the data tuple.

Give the code a try yourself in your python shell in the [terminal](tab-0)

```run
from cassandra.cluster import Cluster

# Connect to the ScyllaDB cluster
cluster = Cluster(['127.0.0.1'])
session = cluster.connect('binance')

# Insert data into the trades table
insert_query = """
INSERT INTO trades (symbol, counter, trade_id, timestamp, price, quantity)
VALUES (%s, %s, %s, %s, %s, %s)
"""
data = ('BTCUSD', 1, 1001, 1638316800, 57000.00, 0.5)
session.execute(insert_query, data)

print("Data inserted successfully.")
```

You can also read the trades back from the database, with similar code as follows:

```run
from cassandra.cluster import Cluster

# Connect to the ScyllaDB cluster
cluster = Cluster(['127.0.0.1'])
session = cluster.connect('binance')

# Select data from the trades table
select_query = "SELECT * FROM trades WHERE symbol = %s"
rows = session.execute(select_query, ('BTCUSD',))

for row in rows:
    print(f"Symbol: {row.symbol}, Counter: {row.counter}, Trade ID: {row.trade_id}, "
          f"Timestamp: {row.timestamp}, Price: {row.price}, Quantity: {row.quantity}")
```

Reading from the table simply:
1. Connects to the ScyllaDB cluster.
2. Prepare a SELECT query to retrieve data from the trades table based on the symbol.
3. Execute the query and iterate over the results to print each row.

Once you are comfortable with the code, `Ctrl-d` to escape the interactive shell, and take a look at the code in your [editor](tab-1):

Building a trade writer
===
Let's break down the code in `trades-writer.py` step by step.

### Imports
The code starts by importing necessary libraries:
1. `asyncio` and `websockets` for handling asynchronous WebSocket connections.
2. `json` for parsing JSON data.
3. `Cluster` from `cassandra.cluster` for connecting to ScyllaDB.

### ScyllaDBClient Class
This class handles the connection to ScyllaDB and inserting trade data into the trades table:
1. `__init__` method: Initializes the connection to ScyllaDB and prepares an `INSERT` statement for inserting trade data.
2. `insert_trade` method: Executes the prepared `INSERT` statement with the trade data.

### BinanceWebSocketClient Class
This class handles the WebSocket connection to Binance and processes incoming trade data:
1. `__init__` method: Initializes the WebSocket client with the symbol to listen to and the ScyllaDB client.
2. `listen_to_trades` method: Connects to the WebSocket and continuously listens for trade messages. Each message is parsed and inserted into the ScyllaDB table.

The main part of the script sets up the WebSocket client and starts listening for trades. To run this code in the background, copy and run the following command in your scylladb [terminal](tab-0):

```run
python3 trades-writer.py &
```

Once that's started you can open up an cqlsh to your server and verify that data is being written to the trades table:

```run
docker exec -it node1 cqlsh
```

```run
SELECT * FROM binance.trades ORDER BY counter DESC LIMIT 50;
SELECT count(*) FROM binance.trades;
```
