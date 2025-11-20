import numpy as np
from utils.math_utils import calculate_d1_d2, normal_cdf

class BlackScholes:
    @staticmethod
    def calculate_call_price(S, K, T, r, sigma):
        """Calculate European call option price"""
        if T <= 0:
            return max(S - K, 0)
        
        d1, d2 = calculate_d1_d2(S, K, T, r, sigma)
        return S * normal_cdf(d1) - K * np.exp(-r * T) * normal_cdf(d2)
    
    @staticmethod
    def calculate_put_price(S, K, T, r, sigma):
        """Calculate European put option price"""
        if T <= 0:
            return max(K - S, 0)
        
        d1, d2 = calculate_d1_d2(S, K, T, r, sigma)
        return K * np.exp(-r * T) * normal_cdf(-d2) - S * normal_cdf(-d1)