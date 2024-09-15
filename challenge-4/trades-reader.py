import os
import plotext as plt
from cassandra.cluster import Cluster
import time
import datetime

class ScyllaDBClient:
    def __init__(self, keyspace='binance', hosts=['127.0.0.1']):
        self.cluster = Cluster(hosts)
        self.session = self.cluster.connect()
        self.session.set_keyspace(keyspace)
        self.fetch_trades_stmt = self.session.prepare("""
            SELECT counter, timestamp, price, quantity FROM trades
            WHERE symbol = ? 
            ORDER BY counter DESC LIMIT ?
        """)

    def fetch_last_trades(self, symbol, limit_trades=1000):
        rows = self.session.execute(self.fetch_trades_stmt, (symbol, limit_trades))
        trades = [(row.counter, row.timestamp, float(row.price), float(row.quantity)) for row in rows]
        return sorted(trades, key=lambda x: x[0])

class TradeDataProcessor:
    @staticmethod
    def generate_tick_bars(trades, tick_size=10):
        ohlc = []
        if not trades:
            print("No trades available")
            return ohlc

        for i in range(0, len(trades), tick_size):
            tick_trades = trades[i:i + tick_size]
            if len(tick_trades) < tick_size:
                break

            prices = [trade[2] for trade in tick_trades]
            open_price = prices[0]
            high_price = max(prices)
            low_price = min(prices)
            close_price = prices[-1]
            timestamp = datetime.datetime.fromtimestamp(tick_trades[0][1] / 1000)
            ohlc.append((timestamp, open_price, high_price, low_price, close_price))

        return ohlc

class CandlestickPlotter:
    @staticmethod
    def plot_candlesticks(ohlc_data):
        if not ohlc_data:
            print("No OHLC data to plot")
            return

        plt.clf()
        plt.theme("dark")
        plt.date_form("H:M:S")

        dates = [ohlc[0] for ohlc in ohlc_data]
        opens = [ohlc[1] for ohlc in ohlc_data]
        highs = [ohlc[2] for ohlc in ohlc_data]
        lows = [ohlc[3] for ohlc in ohlc_data]
        closes = [ohlc[4] for ohlc in ohlc_data]

        data = {
            "Open": opens,
            "High": highs,
            "Low": lows,
            "Close": closes
        }

        date_strings = plt.datetimes_to_string(dates)
        plt.candlestick(date_strings, data)
        plt.title("Candlestick Chart (Tick Bars of 10 Trades)")
        plt.show()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    symbol = 'BTCUSDT'
    db_client = ScyllaDBClient()
    processor = TradeDataProcessor()
    plotter = CandlestickPlotter()

    while True:
        clear_screen()
        trades = db_client.fetch_last_trades(symbol, limit_trades=1000)
        ohlc_data = processor.generate_tick_bars(trades, tick_size=10)
        plotter.plot_candlesticks(ohlc_data)
        time.sleep(10)