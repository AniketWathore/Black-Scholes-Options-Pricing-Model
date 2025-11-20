import threading
import time
import pandas as pd
from datetime import datetime
from data.alpaca_data import AlpacaData
from data.binance_data import BinanceData

class DataStreamer:
    def __init__(self, data_source='alpaca', update_interval=10):
        self.data_source = data_source
        self.update_interval = update_interval  # seconds
        self.is_running = False
        self.subscribers = []
        
        if data_source == 'alpaca':
            self.data_client = AlpacaData()
        elif data_source == 'binance':
            self.data_client = BinanceData()
        
        self.current_prices = {}
        self.price_history = {}
    
    def subscribe(self, callback):
        """Subscribe to price updates"""
        self.subscribers.append(callback)
    
    def notify_subscribers(self, symbol, price, timestamp):
        """Notify all subscribers of price update"""
        for callback in self.subscribers:
            callback(symbol, price, timestamp)
    
    def start_streaming(self, symbols):
        """Start real-time data streaming"""
        self.is_running = True
        self.symbols = symbols
        
        def stream_loop():
            while self.is_running:
                try:
                    for symbol in self.symbols:
                        price = self.data_client.get_current_price(symbol)
                        timestamp = datetime.now()
                        
                        if price is not None:
                            self.current_prices[symbol] = price
                            
                            # Store price history
                            if symbol not in self.price_history:
                                self.price_history[symbol] = []
                            self.price_history[symbol].append({
                                'timestamp': timestamp,
                                'price': price
                            })
                            
                            # Keep only last 100 prices
                            if len(self.price_history[symbol]) > 100:
                                self.price_history[symbol].pop(0)
                            
                            # Notify subscribers
                            self.notify_subscribers(symbol, price, timestamp)
                            
                            print(f"{symbol}: ${price:.2f} at {timestamp.strftime('%H:%M:%S')}")
                    
                    time.sleep(self.update_interval)
                    
                except Exception as e:
                    print(f"Error in streaming loop: {e}")
                    time.sleep(self.update_interval)
        
        # Start streaming in a separate thread
        self.stream_thread = threading.Thread(target=stream_loop)
        self.stream_thread.daemon = True
        self.stream_thread.start()
        print(f"Started real-time streaming for {symbols}")
    
    def stop_streaming(self):
        """Stop real-time data streaming"""
        self.is_running = False
        print("Stopped real-time streaming")
    
    def get_current_price(self, symbol):
        """Get current price from stream"""
        return self.current_prices.get(symbol)
    
    def get_price_history(self, symbol):
        """Get price history for a symbol"""
        return self.price_history.get(symbol, [])