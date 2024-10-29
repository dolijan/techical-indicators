import numpy as np
import get_data
from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt

benchmarking_period = 200
benchmark = "VTI" #here we use a total market index as a benchmark we can also use a S&P 500 ETF such as VOO 
symbol = "AAPL" 

def set_symbol(new_symbol):
    global symbol
    new_symbol = symbol

def set_benchmark(new_benchmark):
    global benchmark
    new_benchmark = benchmark


def set_benchmark_period(new_benchmarking_period):
    benchmarking_period = new_benchmarking_period


def calculate_alpha():
    prices = get_data.get_last_N_weeks_close_price(benchmarking_period, symbol)[::-1]
    benchmark_prices = get_data.get_last_N_weeks_close_price(benchmarking_period, benchmark)[::-1]
    #print(prices)
    #print(benchmark_prices)

    prices = pd.Series(prices).pct_change().dropna()
    benchmark_prices = pd.Series(benchmark_prices).pct_change().dropna()

    #print(prices)
    #print(benchmark_prices)

    regr = LinearRegression()

    regr.fit(np.reshape(benchmark_prices, (-1, 1)), prices)

    alpha = regr.intercept_
    beta = regr.coef_[0] #here we do a simple regression with only one parameter

    plt.scatter(prices, benchmark_prices)
    plt.show()

    print(alpha)
    print(beta)

calculate_alpha()


    
