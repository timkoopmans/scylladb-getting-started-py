import os

import plotext as plt
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import time
import datetime

# Connect to ScyllaDB
def connect_to_scylladb():
    cluster = Cluster(['127.0.0.1'])  # Update with your ScyllaDB node IP address if needed
    session = cluster.connect()
    session.set_keyspace('binance')
    return session

# Fetch the last 100 trades using the highest counters
def fetch_last_trades(session, symbol, limit_trades=1000):
    query = SimpleStatement("""
        SELECT counter, timestamp, price, quantity FROM trades
        WHERE symbol = %s
        ORDER BY counter DESC LIMIT %s
    """)

    rows = session.execute(query, (symbol, limit_trades))
    trades = [(row.counter, row.timestamp, float(row.price), float(row.quantity)) for row in rows]

    # Sort the trades by counter in ascending order
    trades_sorted = sorted(trades, key=lambda x: x[0])
    return trades_sorted

# Generate OHLC data (Open, High, Low, Close) for tick bars (group of 10 trades)
def generate_tick_bars(trades, tick_size=10):
    ohlc = []

    if not trades:
        print("No trades available")
        return ohlc

    for i in range(0, len(trades), tick_size):
        tick_trades = trades[i:i + tick_size]

        if len(tick_trades) < tick_size:
            break  # Skip the last group if it's not a full tick bar

        # Extract prices from trades to form OHLC data
        prices = [trade[2] for trade in tick_trades]

        open_price = prices[0]
        high_price = max(prices)
        low_price = min(prices)
        close_price = prices[-1]

        # Convert timestamp from milliseconds to datetime
        timestamp = datetime.datetime.fromtimestamp(tick_trades[0][1] / 1000)

        ohlc.append((timestamp, open_price, high_price, low_price, close_price))  # Use the timestamp of the first trade

    return ohlc

# Plot candlestick data using plotext
def plot_candlesticks(ohlc_data):
    if not ohlc_data:
        print("No OHLC data to plot")
        return

    plt.clf()
    plt.theme("dark")
    plt.date_form("H:M:S")

    # Separate the data into respective lists for plotting
    dates = [ohlc[0] for ohlc in ohlc_data]
    opens = [ohlc[1] for ohlc in ohlc_data]
    highs = [ohlc[2] for ohlc in ohlc_data]
    lows = [ohlc[3] for ohlc in ohlc_data]
    closes = [ohlc[4] for ohlc in ohlc_data]

    # Prepare the data in the format expected by plotext
    data = {
        "Open": opens,
        "High": highs,
        "Low": lows,
        "Close": closes
    }

    # Convert dates to plotext string format
    date_strings = plt.datetimes_to_string(dates)

    # Now plot the candlestick chart with the data dictionary
    plt.candlestick(date_strings, data)
    plt.title("Candlestick Chart (Tick Bars of 10 Trades)")
    plt.show()

# Function to clear the terminal screen before displaying new data
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Main function to connect, fetch data, and plot
if __name__ == "__main__":
    symbol = 'BTCUSDT'  # Example symbol

    # Connect to ScyllaDB
    session = connect_to_scylladb()

    while True:
        # Clear the terminal screen before printing new data
        clear_screen()

        # Fetch the last 1000 trades using the highest counter values
        trades = fetch_last_trades(session, symbol, limit_trades=1000)

        # Generate OHLC data from trades with tick bars (10 trades per bar)
        ohlc_data = generate_tick_bars(trades, tick_size=10)

        # Plot the candlestick chart
        plot_candlesticks(ohlc_data)

        # Wait for 10 seconds before updating the chart again
        time.sleep(10)
