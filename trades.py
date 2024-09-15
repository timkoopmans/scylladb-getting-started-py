import asyncio
import websockets
import json

async def listen_to_trades(symbol):
    # The Binance WebSocket URL for trade streams
    ws_url = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@trade"

    async with websockets.connect(ws_url) as websocket:
        print(f"Connected to {symbol} trade stream")

        while True:
            try:
                # Receiving data from the WebSocket
                message = await websocket.recv()
                trade = json.loads(message)

                # Parse the received trade data
                price = trade['p']
                quantity = trade['q']
                timestamp = trade['T']
                print(f"Price: {price}, Quantity: {quantity}, Timestamp: {timestamp}")

            except Exception as e:
                print(f"Error: {e}")
                break

# Start the event loop to listen to trades
symbol = 'btcusdt'  # Example: BTC/USDT trades
asyncio.get_event_loop().run_until_complete(listen_to_trades(symbol))
