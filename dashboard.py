import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from data.data_streamer import DataStreamer
from core.black_scholes import BlackScholes
from core.greeks_calculator import GreeksCalculator
from utils.date_utils import calculate_time_to_expiry, get_weekly_expiry
import time
import threading

class OptionChainDashboard:
    def __init__(self):
        self.bs = BlackScholes()
        self.greeks_calc = GreeksCalculator()
        self.data_streamer = None
        self.current_price = None
        self.chain_data = []
        
        # Default parameters
        self.risk_free_rate = 0.07
        self.default_volatility = 0.20
        self.expiry_date = get_weekly_expiry(7)
        
        # Streamlit page config
        st.set_page_config(
            page_title="Live Option Chain Analyzer",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def setup_sidebar(self):
        """Setup the sidebar controls"""
        st.sidebar.title("⚙️ Configuration")
        
        # Data source selection
        data_source = st.sidebar.selectbox(
            "Data Source",
            ["Alpaca", "Binance", "Mock Data"],
            index=2
        )
        
        # Symbol selection
        symbol = st.sidebar.text_input("Symbol", value="AAPL")
        
        # Parameters
        st.sidebar.subheader("Pricing Parameters")
        self.risk_free_rate = st.sidebar.slider(
            "Risk-Free Rate (%)", 
            min_value=0.1, max_value=15.0, value=7.0, step=0.1
        ) / 100
        
        self.default_volatility = st.sidebar.slider(
            "Volatility (%)", 
            min_value=5.0, max_value=100.0, value=20.0, step=1.0
        ) / 100
        
        # Strike range configuration
        st.sidebar.subheader("Strike Configuration")
        strike_range = st.sidebar.slider(
            "Strike Range ($)", 
            min_value=10, max_value=200, value=50, step=5
        )
        
        strike_step = st.sidebar.slider(
            "Strike Step ($)", 
            min_value=1, max_value=20, value=5, step=1
        )
        
        # Update interval
        update_interval = st.sidebar.slider(
            "Update Interval (seconds)", 
            min_value=1, max_value=60, value=5, step=1
        )
        
        # Control buttons
        col1, col2 = st.sidebar.columns(2)
        start_btn = col1.button("Start Live Feed")
        stop_btn = col2.button("Stop Feed")
        
        return {
            'data_source': data_source.lower().replace(' ', '_'),
            'symbol': symbol,
            'strike_range': strike_range,
            'strike_step': strike_step,
            'update_interval': update_interval,
            'start_btn': start_btn,
            'stop_btn': stop_btn
        }
    
    def generate_strikes(self, current_price, strike_range, step):
        """Generate strike prices around current price"""
        if current_price is None:
            return []
            
        start_strike = max(current_price - strike_range, step)
        end_strike = current_price + strike_range
        
        strikes = []
        strike = start_strike
        while strike <= end_strike:
            rounded_strike = round(strike / step) * step
            strikes.append(rounded_strike)
            strike += step
        
        return sorted(set(strikes))
    
    def calculate_option_chain(self, current_price, strike_range, strike_step):
        """Calculate the complete option chain"""
        if current_price is None:
            return []
        
        T = calculate_time_to_expiry(self.expiry_date)
        strikes = self.generate_strikes(current_price, strike_range, strike_step)
        
        chain_data = []
        
        for strike in strikes:
            # Calculate option prices
            call_price = self.bs.calculate_call_price(
                current_price, strike, T, self.risk_free_rate, self.default_volatility
            )
            put_price = self.bs.calculate_put_price(
                current_price, strike, T, self.risk_free_rate, self.default_volatility
            )
            
            # Calculate Greeks for call
            call_greeks = self.greeks_calc.calculate_all_greeks(
                current_price, strike, T, self.risk_free_rate, self.default_volatility, 'call'
            )
            
            # Calculate Greeks for put
            put_greeks = self.greeks_calc.calculate_all_greeks(
                current_price, strike, T, self.risk_free_rate, self.default_volatility, 'put'
            )
            
            # Determine if ATM
            is_atm = abs(current_price - strike) <= strike_step / 2
            
            chain_data.append({
                'Strike': strike,
                'Call Price': call_price,
                'Put Price': put_price,
                'Call Delta': call_greeks['delta'],
                'Put Delta': put_greeks['delta'],
                'Call Gamma': call_greeks['gamma'],
                'Put Gamma': put_greeks['gamma'],
                'Call Theta': call_greeks['theta'],
                'Put Theta': put_greeks['theta'],
                'Call Vega': call_greeks['vega'],
                'Put Vega': put_greeks['vega'],
                'Call Rho': call_greeks['rho'],
                'Put Rho': put_greeks['rho'],
                'ATM': '✅' if is_atm else '',
                'Timestamp': datetime.now()
            })
        
        return chain_data
    
    def display_option_chain_table(self, chain_data):
        """Display the option chain in a professional table format"""
        if not chain_data:
            st.warning("No option chain data available. Please start the live feed.")
            return
        
        df = pd.DataFrame(chain_data)
        
        # Create a professional layout with columns
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.subheader(f"Live Option Chain - {datetime.now().strftime('%H:%M:%S')}")
            
            # Style the dataframe
            styled_df = df.style.format({
                'Strike': '{:.0f}',
                'Call Price': '{:.2f}',
                'Put Price': '{:.2f}',
                'Call Delta': '{:.4f}',
                'Put Delta': '{:.4f}',
                'Call Gamma': '{:.6f}',
                'Put Gamma': '{:.6f}',
                'Call Theta': '{:.4f}',
                'Put Theta': '{:.4f}',
                'Call Vega': '{:.4f}',
                'Put Vega': '{:.4f}',
                'Call Rho': '{:.4f}',
                'Put Rho': '{:.4f}'
            }).apply(self.highlight_atm_rows, axis=1)
            
            # Display the table
            st.dataframe(
                styled_df,
                use_container_width=True,
                height=600,
                hide_index=True
            )
    
    def highlight_atm_rows(self, row):
        """Highlight ATM rows in the dataframe"""
        if row['ATM'] == '✅':
            return ['background-color: #e6f7ff'] * len(row)
        return [''] * len(row)
    
    def display_greeks_charts(self, chain_data):
        """Display charts for Greeks analysis"""
        if not chain_data:
            return
        
        df = pd.DataFrame(chain_data)
        
        st.subheader("Greeks Analysis")
        
        # Create tabs for different Greeks
        tab1, tab2, tab3, tab4 = st.tabs(["Delta & Gamma", "Theta", "Vega", "Rho"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Delta chart
                fig_delta = go.Figure()
                fig_delta.add_trace(go.Scatter(
                    x=df['Strike'], y=df['Call Delta'],
                    mode='lines+markers', name='Call Delta',
                    line=dict(color='green', width=2)
                ))
                fig_delta.add_trace(go.Scatter(
                    x=df['Strike'], y=df['Put Delta'],
                    mode='lines+markers', name='Put Delta',
                    line=dict(color='red', width=2)
                ))
                fig_delta.update_layout(
                    title='Delta vs Strike Price',
                    xaxis_title='Strike Price',
                    yaxis_title='Delta',
                    height=400
                )
                st.plotly_chart(fig_delta, use_container_width=True)
            
            with col2:
                # Gamma chart
                fig_gamma = go.Figure()
                fig_gamma.add_trace(go.Scatter(
                    x=df['Strike'], y=df['Call Gamma'],
                    mode='lines+markers', name='Gamma',
                    line=dict(color='blue', width=2)
                ))
                fig_gamma.update_layout(
                    title='Gamma vs Strike Price',
                    xaxis_title='Strike Price',
                    yaxis_title='Gamma',
                    height=400
                )
                st.plotly_chart(fig_gamma, use_container_width=True)
        
        with tab2:
            # Theta chart
            fig_theta = go.Figure()
            fig_theta.add_trace(go.Scatter(
                x=df['Strike'], y=df['Call Theta'],
                mode='lines+markers', name='Call Theta',
                line=dict(color='orange', width=2)
            ))
            fig_theta.add_trace(go.Scatter(
                x=df['Strike'], y=df['Put Theta'],
                mode='lines+markers', name='Put Theta',
                line=dict(color='purple', width=2)
            ))
            fig_theta.update_layout(
                title='Theta (Daily Time Decay) vs Strike Price',
                xaxis_title='Strike Price',
                yaxis_title='Theta',
                height=400
            )
            st.plotly_chart(fig_theta, use_container_width=True)
        
        with tab3:
            # Vega chart
            fig_vega = go.Figure()
            fig_vega.add_trace(go.Scatter(
                x=df['Strike'], y=df['Call Vega'],
                mode='lines+markers', name='Vega',
                line=dict(color='teal', width=2)
            ))
            fig_vega.update_layout(
                title='Vega vs Strike Price',
                xaxis_title='Strike Price',
                yaxis_title='Vega',
                height=400
            )
            st.plotly_chart(fig_vega, use_container_width=True)
    
    def display_summary_metrics(self, chain_data, current_price):
        """Display summary metrics"""
        if not chain_data:
            return
        
        df = pd.DataFrame(chain_data)
        
        st.subheader("Summary Metrics")
        
        # Find ATM strike
        if current_price:
            atm_strike = min(df['Strike'], key=lambda x: abs(x - current_price))
            atm_data = df[df['Strike'] == atm_strike].iloc[0]
        else:
            atm_strike = None
            atm_data = None
        
        # Create metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if current_price:
                st.metric("Underlying Price", f"${current_price:.2f}")
        
        with col2:
            if atm_strike:
                st.metric("ATM Strike", f"${atm_strike:.0f}")
        
        with col3:
            if atm_data is not None:
                st.metric("ATM Call Price", f"${atm_data['Call Price']:.2f}")
        
        with col4:
            if atm_data is not None:
                st.metric("ATM Put Price", f"${atm_data['Put Price']:.2f}")
        
        with col5:
            if atm_data is not None:
                st.metric("ATM Call Delta", f"{atm_data['Call Delta']:.3f}")
    
    def run(self):
        """Run the main dashboard"""
        st.title("Live Option Chain Analyzer")
        st.markdown("---")
        
        # Setup sidebar
        config = self.setup_sidebar()
        
        # Display current status
        status_placeholder = st.empty()
        
        # Initialize data streamer if starting
        if config['start_btn'] and not hasattr(self, 'streaming_started'):
            self.streaming_started = True
            if config['data_source'] != 'mock_data':
                self.data_streamer = DataStreamer(config['data_source'], config['update_interval'])
                self.data_streamer.subscribe(self.on_price_update)
                self.data_streamer.start_streaming([config['symbol']])
            else:
                # Use mock data for demonstration
                self.current_price = 180.50  # Mock price
                self.start_mock_streaming(config)
        
        if config['stop_btn'] and hasattr(self, 'streaming_started'):
            self.streaming_started = False
            if self.data_streamer:
                self.data_streamer.stop_streaming()
        
        # Calculate and display option chain
        if hasattr(self, 'streaming_started') and self.streaming_started:
            status_placeholder.success(f"Live feed running - {config['symbol']}")
            
            # Calculate option chain
            chain_data = self.calculate_option_chain(
                self.current_price, 
                config['strike_range'], 
                config['strike_step']
            )
            
            # Display components
            self.display_summary_metrics(chain_data, self.current_price)
            self.display_option_chain_table(chain_data)
            self.display_greeks_charts(chain_data)
            
            # Auto-refresh
            time.sleep(config['update_interval'])
            st.rerun()
        else:
            status_placeholder.info("Live feed stopped - Configure and click 'Start Live Feed'")
    
    def on_price_update(self, symbol, price, timestamp):
        """Callback for price updates"""
        self.current_price = price
    
    def start_mock_streaming(self, config):
        """Start mock data streaming for demonstration"""
        def mock_stream():
            import random
            base_price = 180.50
            while hasattr(self, 'streaming_started') and self.streaming_started:
                # Simulate price movement
                movement = random.uniform(-2, 2)
                self.current_price = base_price + movement
                time.sleep(config['update_interval'])
        
        self.mock_thread = threading.Thread(target=mock_stream)
        self.mock_thread.daemon = True
        self.mock_thread.start()

def main():
    dashboard = OptionChainDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()