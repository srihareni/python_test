#packages
import pandas as pd
from pandas import datetime
import numpy as np


import matplotlib
import matplotlib.pyplot as plt
%matplotlib inline
plt.style.use('fivethirtyeight')

import seaborn as sns

from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15,9    #figure size

#importing the data
path = 'C:/Users/SRIHARINI/Desktop/dat'

TCS = pd.read_csv('C:/Users/SRIHARINI/Desktop/dat/TCS.csv', parse_dates=['Date'])

INFY = pd.read_csv('C:/Users/SRIHARINI/Desktop/dat/INFY.csv', parse_dates=['Date'])

NIFTY = pd.read_csv('C:/Users/SRIHARINI/Desktop/dat/nifty_it.csv', parse_dates=['Date'])



stocks = [TCS, INFY, NIFTY]


TCS.name = 'TCS'
INFY.name = 'INFY'
NIFTY.name = 'NIFTY_IT'
TCS["Date"] = pd.to_datetime(TCS["Date"])
INFY["Date"] = pd.to_datetime(INFY["Date"])
NIFTY["Date"] = pd.to_datetime(NIFTY["Date"])

#extracting the data
def build_features(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df.Date.dt.month
    df['Day'] = df.Date.dt.day
    df['WeekOfYear'] = df.Date.dt.weekofyear
    
for i in range(len(stocks)):
    # print(stocks[i])
    build_features(stocks[i])

TCS.shape #for checking new features

#PART - 1
#Create 4,16,....,52 week moving average(closing price) for each stock and index. This should happen through a function.

def movingaverage(values, m):
   """caluculate average of m observations
      m-rolling window 
   """
return np.average(values[-m:])

def put_index(stock):
    stock.index = stock['Date']
    return stock
    
put_index(TCS)
put_index(INFY)
put_index(NIFTY)
    
    
    
    
