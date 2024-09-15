import asyncio
import websockets
import json
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

# Function to connect to ScyllaDB
def connect_to_scylladb():
    cluster = Cluster(['127.0.0.1'])  # Update with your ScyllaDB node IP address if needed
    session = cluster.connect()
    session.set_keyspace('binance')
    return session

# Function to insert trade data into ScyllaDB and increment the counter
def insert_trade(session, trade, counter):
    query = SimpleStatement("""
        INSERT INTO trades (symbol, counter, trade_id, price, quantity, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
    """)
    session.execute(query, (trade['s'], counter, trade['t'], float(trade['p']), float(trade['q']), trade['T']))

# Function to listen to trades from Binance WebSocket and store them in ScyllaDB
async def listen_to_trades(symbol, session):
    ws_url = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@trade"
    counter = 0  # Initialize counter to track trades

    async with websockets.connect(ws_url) as websocket:
        print(f"Connected to {symbol} trade stream")

        while True:
            try:
                # Receiving data from WebSocket
                message = await websocket.recv()
                trade = json.loads(message)

                # Increment counter for each trade
                counter += 1

                # Insert the trade data into ScyllaDB with the updated counter
                insert_trade(session, trade, counter)

                # Print the received trade data
                print(f"Inserted Trade - Counter: {counter}, ID: {trade['t']}, Price: {trade['p']}, Quantity: {trade['q']}, Timestamp: {trade['T']}")

            except Exception as e:
                print(f"Error: {e}")
                break

# Start the event loop and connect to ScyllaDB
if __name__ == "__main__":
    symbol = 'btcusdt'  # Example: BTC/USDT trades

    # Connect to ScyllaDB
    session = connect_to_scylladb()

    # Start listening to trades and writing to ScyllaDB
    asyncio.get_event_loop().run_until_complete(listen_to_trades(symbol, session))
