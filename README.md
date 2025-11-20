# Black-Scholes Options Pricing Model

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

Black-Scholes Options Pricing Model for European Options with Option Greeks. This web application provides real-time calculations and graphical analysis of options pricing using the Black-Scholes-Merton model.


## 📋 Project Description

This project implements the Black-Scholes-Merton model for pricing European-style options. It features an intuitive web interface built with Streamlit that allows users to:
- Calculate theoretical prices for call and put options
- Visualize Option Greeks (Delta, Gamma, Theta, Vega, Rho)
- Analyze how option prices change with underlying parameters
- Understand the sensitivity of options to various market factors

## 🧮 Black-Scholes Model

The Black-Scholes model, also known as the Black-Scholes-Merton (BSM) model, is a fundamental concept in modern financial theory. This mathematical equation estimates the theoretical value of derivatives, accounting for the impact of time and other risk factors.

### Model Inputs
The Black-Scholes equation requires five primary variables:
- **Volatility (σ)** - The volatility of the underlying asset
- **Underlying Price (S)** - Current price of the underlying asset
- **Strike Price (K)** - Strike price of the option
- **Time to Expiration (T)** - Time until option expiration (in years)
- **Risk-Free Rate (r)** - Risk-free interest rate

### Black-Scholes Model Assumptions

The model operates under these key assumptions:
1. No dividends are paid out during the option's life
2. Markets are efficient and random (market movements cannot be predicted)
3. No transaction costs in buying the option
4. The risk-free rate and volatility are known and constant
5. Returns on the underlying asset are log-normally distributed
6. The option is European and can only be exercised at expiration

## 📊 Mathematical Formulas

### Call and Put Option Prices

**Call Option (C):**
C = S × N(d1) - K × e^(-rT) × N(d2)

**Put Option (P):**
P = K × e^(-rT) × N(-d2) - S × N(-d1)

**Where:**
d1 = [ln(S/K) + (r + σ²/2)T] / (σ√T)
d2 = d1 - σ√T


- `N(x)` = Cumulative distribution function of standard normal distribution
- `S` = Current underlying price
- `K` = Strike price
- `r` = Risk-free interest rate
- `T` = Time to expiration (in years)
- `σ` = Volatility

## 🎯 The Option Greeks

"The Greeks" measure the sensitivity of an option's value to changes in underlying parameters. They are partial derivatives of the price with respect to each parameter.

### Greek Formulas

- **Delta (Δ)**: Sensitivity to underlying price changes
- **Gamma (Γ)**: Sensitivity of Delta to underlying price changes
- **Theta (Θ)**: Sensitivity to time decay
- **Vega (ν)**: Sensitivity to volatility changes
- **Rho (ρ)**: Sensitivity to interest rate changes

## 🛠️ Installation

To run this project locally, follow these steps:

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/AniketWathore/Black-Scholes-Options-Pricing-Model.git
   cd Black-Scholes-Options-Pricing-Model
2. Create a virtual environment (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install required packages
   ```bash
   pip install -r requirements.txt

4. Run the application
   ```bash
   python main.py

## 🎮 Usage

1. Input Parameters: Enter the required parameters in the sidebar:

   - Underlying Price
   
   - Strike Price
   
   - Time to Expiration (in years)
   
   - Risk-Free Rate (as decimal)
   
   - Volatility (as decimal)

2. View Results: The main panel will display:

   - Call and Put option prices

   - Option Greeks values

   - Interactive sensitivity charts

3. Analysis: Use the visualization tools to understand how different factors affect option pricing.


## 🧪 Features

- Real-time Black-Scholes calculations

- Complete Option Greeks analysis

- Interactive parameter sensitivity charts

- User-friendly web interface


## 📚 Dependencies

The project uses the following main libraries:

streamlit - Web application framework

numpy - Numerical computations

pandas - Data manipulation

plotly - Interactive visualizations

scipy - Statistical functions including Normal CDF


## 📖 Sources and References

- Black-Scholes Model Explanation: Wikipedia and Investopedia

- Formula References: Macroption

- Financial Mathematics: Hull, J.C. - "Options, Futures and Other Derivatives"

