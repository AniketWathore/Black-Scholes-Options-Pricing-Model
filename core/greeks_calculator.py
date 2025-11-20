from utils.math_utils import calculate_d1_d2, normal_cdf
from scipy.stats import norm
import numpy as np

class GreeksCalculator:
    @staticmethod
    def calculate_delta(S, K, T, r, sigma, option_type='call'):
        """Calculate option delta"""
        d1, _ = calculate_d1_d2(S, K, T, r, sigma)
        
        if option_type == 'call':
            return normal_cdf(d1)
        else:  # put
            return normal_cdf(d1) - 1
    
    @staticmethod
    def calculate_gamma(S, K, T, r, sigma):
        """Calculate option gamma"""
        d1, _ = calculate_d1_d2(S, K, T, r, sigma)
        return norm.pdf(d1) / (S * sigma * np.sqrt(T))
    
    @staticmethod
    def calculate_all_greeks(S, K, T, r, sigma, option_type='call'):
        """Calculate all Greeks for an option"""
        d1, d2 = calculate_d1_d2(S, K, T, r, sigma)
        
        greeks = {}
        greeks['delta'] = GreeksCalculator.calculate_delta(S, K, T, r, sigma, option_type)
        greeks['gamma'] = GreeksCalculator.calculate_gamma(S, K, T, r, sigma)
        
        # Theta (daily)
        theta_term1 = - (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
        if option_type == 'call':
            theta_term2 = - r * K * np.exp(-r * T) * normal_cdf(d2)
        else:
            theta_term2 = + r * K * np.exp(-r * T) * normal_cdf(-d2)
        greeks['theta'] = (theta_term1 + theta_term2) / 365.0
        
        # Vega (for 1% vol change)
        greeks['vega'] = S * norm.pdf(d1) * np.sqrt(T) / 100
        
        # Rho (for 1% rate change)
        if option_type == 'call':
            greeks['rho'] = (K * T * np.exp(-r * T) * normal_cdf(d2)) / 100
        else:
            greeks['rho'] = (-K * T * np.exp(-r * T) * normal_cdf(-d2)) / 100
        
        return greeks