import asyncio
import websockets
import json
from cassandra.cluster import Cluster

class ScyllaDBClient:
    def __init__(self, keyspace='binance', hosts=['127.0.0.1']):
        self.cluster = Cluster(hosts)
        self.session = self.cluster.connect()
        self.session.set_keyspace(keyspace)
        self.insert_trade_stmt = self.session.prepare("""
            INSERT INTO trades (symbol, counter, trade_id, price, quantity, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """)

    def insert_trade(self, trade, counter):
        self.session.execute(self.insert_trade_stmt, (trade['s'], counter, trade['t'], float(trade['p']), float(trade['q']), trade['T']))

class BinanceWebSocketClient:
    def __init__(self, symbol, db_client):
        self.symbol = symbol.lower()
        self.db_client = db_client
        self.ws_url = f"wss://stream.binance.com:9443/ws/{self.symbol}@trade"
        self.counter = 0

    async def listen_to_trades(self):
        async with websockets.connect(self.ws_url) as websocket:
            while True:
                try:
                    message = await websocket.recv()
                    trade = json.loads(message)
                    self.counter += 1
                    self.db_client.insert_trade(trade, self.counter)
                except Exception as e:
                    print(f"Error: {e}")
                    break

if __name__ == "__main__":
    symbol = 'btcusdt'
    db_client = ScyllaDBClient()
    ws_client = BinanceWebSocketClient(symbol, db_client)
    asyncio.get_event_loop().run_until_complete(ws_client.listen_to_trades())