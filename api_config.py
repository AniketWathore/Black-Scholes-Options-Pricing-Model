import finnhub
from binance.client import Client
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.live import StockDataStream

# Finnhub API Configuration
FINNHUB_CONFIG = {
    'api_key': 'xxx'
}

# Alpaca Api Configuration
ALPACA_CONFIG = {
    'api_key' : 'xxx',
    'client_id' : 'xxx',
    'api_secret': 'xxx',
    'redirect_uri': 'https://paper-api.alpaca.markets/v2'
}

# Binance Api Configuration
BINANCE_CONFIG = {
    'api_key' : 'xxx',
    'api_secret' : 'xxx'
}


# Trading Parameters
SYMBOLS = {
    'alpaca': ['AAPL', 'TSLA', 'AMD'],
    'binance': ['BTCUSDT', 'ETHUSDT'],
    'finnhub': ['AAPL', 'MSFT']
}

INTERVALS = {
    '1min': '1min',
    '5min': '5min', 
    '15min': '15min',
    '1h': '1h',
    '1d': '1d'
}