import streamlit.web.cli as stcli
import sys
import os

def main():
    """Launch the Streamlit dashboard"""
    try:
        print("Starting Option Chain Dashboard...")
        print("Opening web browser at http://localhost:8501")
        
        # Set the command line arguments for Streamlit
        sys.argv = [
            "streamlit", "run", 
            "dashboard.py",
            "--server.port=8501",
            "--server.address=0.0.0.0",
            "--browser.serverAddress=localhost"
        ]
        
        # Run Streamlit
        sys.exit(stcli.main())
        
    except Exception as e:
        print(f"Error starting dashboard: {e}")
        print("Make sure Streamlit is installed: pip install streamlit plotly")

if __name__ == "__main__":
    main()