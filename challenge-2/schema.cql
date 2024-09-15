CREATE KEYSPACE IF NOT EXISTS binance WITH replication = {
    'class': 'NetworkTopologyStrategy',
    'replication_factor': 3
    };

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
