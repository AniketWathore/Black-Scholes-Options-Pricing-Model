from api_config import BINANCE_CONFIG
from binance.client import Client
import pandas as pd

class BinanceData:
    def __init__(self):
        self.client = Client(BINANCE_CONFIG['api_key'], BINANCE_CONFIG['api_secret'])
    
    def fetch_klines(self, symbol, interval, limit=50):
        """
        Fetches live klines (candlestick data) from Binance.
        """
        klines = self.client.get_klines(symbol=symbol, interval=interval, limit=limit)
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        
        # Convert to proper data types
        df['close'] = df['close'].astype(float)
        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['volume'] = df['volume'].astype(float)
        
        return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    
    def get_current_price(self, symbol):
        """Get current cryptocurrency price"""
        df = self.fetch_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, limit=1)
        return float(df['close'].iloc[-1]) if not df.empty else None