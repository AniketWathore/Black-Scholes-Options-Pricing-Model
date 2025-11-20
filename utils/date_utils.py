from datetime import datetime, date, timedelta

def calculate_time_to_expiry(expiry_date, current_date=None):
    """Calculate time to expiry in years"""
    if current_date is None:
        current_date = datetime.now()
    
    # Convert both to datetime for consistent subtraction
    if isinstance(expiry_date, date) and not isinstance(expiry_date, datetime):
        expiry_date = datetime.combine(expiry_date, datetime.min.time())
    
    time_delta = expiry_date - current_date
    return max(time_delta.total_seconds() / (365.25 * 24 * 3600), 0)  # Ensure non-negative

def get_weekly_expiry(days=7):
    """Get expiry date 7 days from now"""
    return datetime.now() + timedelta(days=days)

def is_market_open():
    """Check if market is currently open (basic implementation)"""
    now = datetime.now()
    # US Market hours (9:30 AM - 4:00 PM EST)
    market_open = now.replace(hour=19, minute=00, second=0, microsecond=0)
    market_close = now.replace(hour=3, minute=00, second=0, microsecond=0)
    
    return market_open <= now <= market_close and now.weekday() < 5