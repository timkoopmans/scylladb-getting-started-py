The application is a simple library which pulls real time trade information from a cryptocurrency exchange, using websockets. To consume trades from Binance's WebSocket API, you can use the websockets package in Python.

Take a look at the application code for this example in `trades.py`

A WebSocket URL is constructed using the Binance stream endpoint `wss://stream.binance.com:9443/ws/` followed by `{symbol}@trade`. For example, if you want to listen to BTC/USDT trades, you will use `btcusdt@trade`.

The WebSocket connection receives trade data in real-time, and this is parsed using json.loads() to extract fields such as price (p), quantity (q), and timestamp (T).

The while loop keeps the connection open, continuously receiving trade messages until an exception occurs.

In your [terminal](tab-1), copy and run the following code to see how this API works in real time:

```run
python3 trades.py
```

The output should look something like:

```
Connected to btcusdt trade stream
Price: 60226.01000000, Quantity: 0.00050000, Timestamp: 1726370435104
Price: 60226.01000000, Quantity: 0.00101000, Timestamp: 1726370436089
Price: 60226.00000000, Quantity: 0.00236000, Timestamp: 1726370436213
Price: 60226.00000000, Quantity: 0.00332000, Timestamp: 1726370436213
```

Next you will learn how to write these trade events to a table in ScyllaDB.