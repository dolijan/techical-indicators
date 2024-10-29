import requests, os, json, datetime, numpy as np, sys

#here begins the real shit
api_key = "REDACTED"

#given a ticker symbol, return the current price of the security
def get_current_security_price(symbol):
    api_request = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={api_key}"
    price_raw = requests.get(api_request).json()
    return float(price_raw['price'])


#get the closing price of the security in the last N days in an array
def get_last_N_days_close_price(n, symbol):
    api_request = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize={n}&apikey={api_key}" 
    prices_raw = requests.get(api_request).json()
    closing_prices = []
    for item in prices_raw['values'] :
        closing_prices.append(float(item['close']))
    return closing_prices

#get the closing price of the security in the last N weeks in an array
def get_last_N_weeks_close_price(n, symbol):
    api_request = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1week&outputsize={n}&apikey={api_key}" 
    prices_raw = requests.get(api_request).json()
    closing_prices = []
    for item in prices_raw['values'] :
        closing_prices.append(float(item['close']))
    return closing_prices


#get the open price of a security in the last N days in an array
def get_last_N_days_open_price(n, symbol):
    api_request = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize={n}&apikey={api_key}" 
    prices_raw = requests.get(api_request).json()
    open_prices = []
    for item in prices_raw['values'] :
        open_prices.append(float(item['open']))
    return open_prices

#get the high price of a security in the last N days in an array
def get_last_N_days_high_price(n, symbol):
    api_request = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize={n}&apikey={api_key}" 
    prices_raw = requests.get(api_request).json()
    high_prices = []
    for item in prices_raw['values'] :
        high_prices.append(float(item['high']))
    return high_prices

#get the low price of a security in the last N days in an array
def get_last_N_days_low_price(n, symbol):
    api_request = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize={n}&apikey={api_key}" 
    prices_raw = requests.get(api_request).json()
    high_prices = []
    for item in prices_raw['values'] :
        low_prices.append(float(item['low']))
    return low_prices

#get the volume, low, high, open, close of  a security
def get_security_info_last_N_days(n, symbol):
    api_request = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize={n}&apikey={api_key}" 
    prices_raw = requests.get(api_request).json()
    return prices_raw['values']


#this is insane but it is not used anywhere AFAIK
def get_last_N_days_dates(n, symbol):
    api_request = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize={n}&apikey={api_key}" 
    prices_raw = requests.get(api_request).json()
    dates = []
    for item in prices_raw['values'] :
        dates.append(item['datetime'])
    return dates





