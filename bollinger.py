import numpy as np
import get_data
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
#we need this for plotting candlestick charts
import mplfinance as mpf

import sys

k = 2
n = 20
symbol = "KO"

#number of standard deviations from moving average
def get_k():
    return 2

#n is the number of days for which we will get the moving average
def get_n():
    return 20

def set_symbol(new_symbol):
    global symbol
    symbol = new_symbol


#this method will calculate a simple moving average provided a numpy array of closing prices
def calculate_sma(closing_prices):
    period = len(closing_prices) - n
    sma = []
    current_sum = 0
    for i in range(n):
        current_sum += closing_prices[i]
    for i in range(n, n + period):
        sma.append(current_sum / n)
        current_sum -= closing_prices[i - n]
        current_sum += closing_prices[i]
    return sma

#given a numpy array of closing prices, calculate a N period standard deviation on each day
#we are gonna be using Bessel's correction here so we will have one degree of freedom
def calculate_std(closing_prices):
    period = len(closing_prices) - n
    std = []
    for i in range(n, period + n):
        std.append(np.std(closing_prices[(i - n) : i], ddof = 1))
    return std



#we plot bollinger bands for an amount of dates specified in the period variable
def plot_for_last_n_days(period):
    #we need some padding on thre left side of the array to calculate the moving average
    #TODO: make this like god intended, also finish plotting nicely the bollinger bands
    security_info = get_data.get_security_info_last_N_days(period + n, symbol)

    closing_prices = [ float(security_info[i]['close']) for i in range(period + n)][::-1]
    opening_prices = [ float(security_info[i]['open']) for i in range(period + n)][::-1]
    high_prices =    [ float(security_info[i]['high']) for i in range(period + n)][::-1]
    low_prices =   [ float(security_info[i]['close']) for i in range(period + n)][::-1]
    dates = [security_info[i - n]['datetime'] for i in range(n, period  + n)]


    closing_prices = np.array(closing_prices)
    #print(closing_prices)

    #dates = get_data.get_last_N_days_dates(period, symbol)

    sma = calculate_sma(closing_prices)
    std = calculate_std(closing_prices)

    #print("Now outputing the standard deviation array")
    #print(std)
    
    
    #WARNING: Generative AI used below


    #get dates in mpf supported format
    dates_for_mpf = pd.date_range(pd.to_datetime('today').normalize(), periods = period)
    data = {
            'Open': opening_prices[n:],
            'High': high_prices[n:],
            'Low': low_prices[n:],
            'Close': closing_prices[n:]
    }
    df = pd.DataFrame(data, index=reversed([pd.to_datetime(item) for item in dates]))


    #print(df)
    

    fig, ax = plt.subplots(figsize=(10, 6))
    mpf.plot(df, type='candle', ax=ax, style='charles', show_nontrading=False)

    ax.grid(True)

    # Creating a Seaborn line plot
    sns.set(style="whitegrid")
    #plt.figure(figsize=(8, 5))
    sns.lineplot(x=reversed(dates), y=sma,ax = ax, label = f'SMA for the last {n} days')
    sns.lineplot(x=reversed(dates),y = [sma[i] + 2 * std[i] for i in range(period)],ax = ax, label = f'SMA + {k} * SD')
    sns.lineplot(x=reversed(dates),y = [sma[i] - 2 * std[i] for i in range(period)] ,ax = ax, label = f'SMA - {k} * SD')

    #this max is just a hack becaue if we query for a low value of dates we might get a zero
    subset_indices = [dates[i] for i in  reversed(range(0, len(dates), max(len(dates) // 7, 1))) ]
    plt.xticks(ticks=subset_indices, labels=subset_indices)

    # Adding labels and titlee
    plt.title(f'Bollinger bands for {symbol} for the last {period} days')
    plt.xlabel('Date')
    plt.ylabel('Price')

    # return the plot??
    return plt


def get_analysis():
    current_price = get_data.get_current_security_price(symbol)
    
    security_info = get_data.get_security_info_last_N_days(n + 1, symbol)

    closing_prices = [ float(security_info[i]['close']) for i in range(n + 1)][::-1]
    closing_prices = np.array(closing_prices)
    
    sma = calculate_sma(closing_prices)
    std = calculate_std(closing_prices)

    if current_price < sma[-1] - 2 * std[-1]:
        print("BELOW LOWER BOLLINGER BAND")
        return 1 #this exit code signifies that we should buy
    elif current_price > sma[-1] + 2 * std[-1]:
        print("ABOVE UPPER BOLLINGER BAND")
        return -1 #this exit code signifies that we shall sell
    else:
        print("BETWEEN BOLLINGER BANDS")
        return 0 #no activity
        
