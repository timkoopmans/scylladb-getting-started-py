In the last challenge you learned how to read and write data using the python driver.  Now that you're comfortable with the basics, lets learn how to build a trade reader for the application that prints out ticker data to the screen.

Building a trade reader
===
Let's break down the code in `trades-reader.py` step by step.

### Imports
The code starts by importing necessary libraries:
1. `os` for clearing the terminal screen.
2. `plotext` for plotting candlestick charts in the terminal.
3. `cassandra.cluster` for connecting to ScyllaDB.
4. `time` and `datetime` for handling time-related operations.

### ScyllaDBClient Class
This class handles the connection to ScyllaDB and reading trade data from the trades table:
1. `__init__` method: Initializes the connection to ScyllaDB and prepares a `SELECT` statement for fetching trade data.
2. `fetch_last_trades` method: Executes the prepared `SELECT` statement to fetch the latest trades and returns them sorted by the counter.

### TradeDataProcessor Class
This class processes trade data to generate OHLC (Open, High, Low, Close) data for candlestick charts:
1. `generate_tick_bars` method: Converts trade data into OHLC data based on a specified tick size.

### CandlestickPlotter Class
This class handles plotting the OHLC data as candlestick charts:
1. `plot_candlesticks` method: Plots the OHLC data as a candlestick chart using plotext.

The main part of the script fetches trade data, processes it, and plots it in a loop. To run this code, copy and run the following command in your scylladb [terminal](tab-0):

```run
python3 trades-reader.py
```

Once that's started you should be able to see candlestick data at the tick level (10 trades per tick) in your terminal.