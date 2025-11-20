import numpy as np
from scipy.stats import norm

def calculate_d1_d2(S, K, T, r, sigma):
    """Calculate d1 and d2 for Black-Scholes"""
    if T <= 0:
        return 0, 0
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2

def normal_cdf(x):
    """Standard normal cumulative distribution function"""
    return norm.cdf(x)