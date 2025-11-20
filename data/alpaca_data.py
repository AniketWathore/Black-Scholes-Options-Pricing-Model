from api_config import ALPACA_CONFIG, SYMBOLS
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
import pandas as pd

class AlpacaData:
    def __init__(self):
        try:
            self.trading_client = TradingClient(
                ALPACA_CONFIG['api_key'], 
                ALPACA_CONFIG['api_secret'], 
                paper=True
            )
            self.data_client = StockHistoricalDataClient(
                ALPACA_CONFIG['api_key'], 
                ALPACA_CONFIG['api_secret']
            )
            print("Alpaca client initialized successfully")
        except Exception as e:
            print(f"Failed to initialize Alpaca client: {e}")
            self.data_client = None
    
    def get_account_info(self):
        """Get trading account information"""
        if not self.data_client:
            return "Alpaca client not initialized"
        try:
            return self.trading_client.get_account()
        except Exception as e:
            return f"Error getting account info: {e}"
    
    def get_historical_data(self, symbol, timeframe='5min', days=7):
        """Fetch historical OHLCV data"""
        if not self.data_client:
            print("Alpaca client not initialized - returning mock data")
            # Return mock data for testing
            return self._get_mock_data(symbol)
        
        end_date = datetime.now() - timedelta(minutes=15)
        start_date = end_date - timedelta(days=days)
        
        try:
            request_params = StockBarsRequest(
                symbol_or_symbols=symbol,
                timeframe=TimeFrame(5, TimeFrame.Minute) if timeframe == '5min' else TimeFrame.Day,
                start=start_date,
                end=end_date,
                limit=10000,
                feed="iex"
            )
            
            bars = self.data_client.get_stock_bars(request_params)
            df = bars.df.reset_index()
            
            if 'symbol' in df.columns:
                df = df[df['symbol'] == symbol]
            
            return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
        except Exception as e:
            print(f"Error fetching historical data for {symbol}: {e}")
            return self._get_mock_data(symbol)
    
    def get_current_price(self, symbol):
        """Get current stock price"""
        try:
            data = self.get_historical_data(symbol, '5min', 1)
            if data is not None and not data.empty:
                return float(data['close'].iloc[-1])
            else:
                # Return mock price if no data
                mock_prices = {'AAPL': 180.50, 'TSLA': 250.75, 'AMD': 120.30}
                return mock_prices.get(symbol, 100.00)
        except Exception as e:
            print(f"Error getting current price for {symbol}: {e}")
            # Return mock price
            mock_prices = {'AAPL': 180.50, 'TSLA': 250.75, 'AMD': 120.30}
            return mock_prices.get(symbol, 100.00)
    
    def _get_mock_data(self, symbol):
        """Generate mock data for testing"""
        dates = pd.date_range(end=datetime.now(), periods=100, freq='5min')
        mock_prices = {'AAPL': 180, 'TSLA': 250, 'AMD': 120}
        base_price = mock_prices.get(symbol, 100)
        
        data = {
            'timestamp': dates,
            'open': [base_price] * len(dates),
            'high': [base_price * 1.01] * len(dates),
            'low': [base_price * 0.99] * len(dates),
            'close': [base_price] * len(dates),
            'volume': [1000000] * len(dates)
        }
        return pd.DataFrame(data)