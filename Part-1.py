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

weeks = [4, 16, 28, 40, 52]
def put_index(stock):
    stock.index = stock['Date']
    return stock
    
put_index(TCS)
put_index(INFY)
put_index(NIFTY)

def timeseriesplotting(stock, weeks = [4, 16, 28, 40, 52]):
    
    dummytimeseries = pd.DataFrame()
    # First Resampling into Weeks format to calculate for weeks
    dummytimeseries['Close'] = stock['Close'].resample('W').mean() 
     
    for i in range(len(weeks)):
        moving_average = dummytimeseries['Close'].rolling(weeks[i]).mean() # M.A using inbuilt function
        dummytimeseries[" moving average of first " + str(weeks[i])+ " Weeks"] = moving_average
        print('Moving Averages of {0} weeks: \n\n {1}' .format(weeks[i], dummytimeseries['Close']))
    dummytimeseries.plot(title="Moving Averages of {} \n\n" .format(stock.name))

timeseriesplotting(NIFTY)
timeseriesplotting(TCS)  
timeseriesplotting(INFY)    
    
###2.Create rolling window of size 10 on each stock/index. Handle unequal time series due to stock market holidays.
###You should look to increase your rolling window size to 75 and see how the data looks like.   
###Remember they will create stress on your laptop RAM load. ( Documentation you might need: http://in.mathworks.com/help/econ/rolling-window-estimation-of-state-space-models.html)
###3. Create the following dummy time series:
###   3.1 Volume shocks - If volume traded is 10% higher/lower than previous day - make a 0/1 boolean time series for shock, 0/1 dummy-coded time series for direction of shock.
###   3.2 Price shocks - If closing price at T vs T+1 has a difference > 2%, then 0/1 boolean time series for shock, 0/1 dummy-coded time series for direction of shock.
###   3.3 Pricing black swan - If closing price at T vs T+1 has a difference > 2%, then 0/1 boolean time series for shock, 0/1 dummy-coded time series for direction of shock.
###   3.4 Pricing shock without volume shock - based on points a & b - Make a 0/1 dummy time series.
# For the question two, we have increase the rolling window size from 10 to 75. For rolling window we need to resample as per days.
#by considering only the stock market holidays(i.e., saturdays and sundays - stock market holidays)withpout special holidays instead of using resample() we use resample.Resampler.asfreq() function.
#this is because it provide us option of padding (backwardfill/forwardfill missing values "not NANs" )
#source: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.asfreq.html We are using this, because on saturdays and sundays, market remains closed, so friday's close price could be forwarded in closing days.


TCS = TCS.asfreq('D', method ='pad')        # pad-fill : forward-fill
INFY = INFY.asfreq('D', method ='pad')
NIFTY = NIFTY.asfreq('D', method ='pad')


TCS.name = 'TCS'
INFY.name = 'INFY'
NIFTY.name = 'NIFTY_IT'



#poltting rolling window
def rollingwindow_plotting(stock, win = [10, 75]):
    
    dummyrollingwindow = pd.DataFrame()
    
    dummyrollingwindow['Close'] = stock['Close']
     
    for i in range(len(win)):
        moving_average = dummyrollingwindow['Close'].rolling(win[i]).mean() # M.A using predefined function
        dummyrollingwindow[" moving average of " + str(win[i])+ " Roll Window"] = moving_average
        print('Moving Averages of {0} weeks: \n\n {1}' .format(win[i], dummyrollingwindow['Close']))
    dummyrollingwindow.plot(title="Moving Averages for {} \n\n" .format(stock.name))
    
rollingwindow_plotting(TCS)
rollingwindow_plotting(INFY)
rollingwindow_plotting(NIFTY)

##Volumeshocks
def volumeshocks(stock):
    """
    'Volume' - Vol_t
    'Volume next day - vol_t+1
    
    """
    stock["vol_t+1"] = stock.Volume.shift(1)  #next rows value
    
    stock["volumeshock"] = ((abs(stock["vol_t+1"] - stock["Volume"])/stock["Volume"]*100)  > 10).astype(int)
    
    return stock
volumeshocks(TCS)
volumeshocks(INFY)
volumeshocks(NIFTY)

##Volume Shock Direction

def directionfunction(stock):
    
    # considerng only shock - 1 valued rows.
    # 0 - negative and 1- positive
    if stock["volumeshock"] == 0:
        pass
    else:
        if (stock["vol_t+1"] - stock["Volume"]) < 0:
            return 0
        else:
            return 1
       
def volumeshockdirection(stock):
    stock['VOLUMESHOCKDIRECTION'] = 'Nan'
    stock['VOLUMESHOCKDIRECTION'] = stock.apply(directionfunction, axis=1)
    return stock
volumeshockdirection(TCS)
volumeshockdirection(INFY)
volumeshockdirection(NIFTY)

##Price shocks

def priceshocks(stock):
    """
    'ClosePrice' - Close_t
    'Close Price next day - vol_t+1
    
    """
    stock["price_t+1"] = stock.Close.shift(1)  #next rows value
    
    stock["priceshock"] = (abs((stock["price_t+1"] - stock["Close"])/stock["Close"]*100)  > 2).astype(int)
    
    stock["priceblackswan"] = stock['priceshock'] # Since both had same data anad info/
    
    return stock

##Price Shock Direction and Black Swan shock direction (both same)

def directionfunctionprice(stock):
    
    # considerng only shock - 1 valued rows.
    # 0 - negative and 1- positive
    if stock["priceshock"] == 0:
        pass
    else:
        if (stock["price_t+1"] - stock["Close"]) < 0:
            return 0
        else:
            return 1
def priceshockdirection(stock):
    stock['PRICESHOCKDIRECTION'] = 'Nan'
    stock['PRICESHOCKDIRECTION'] = stock.apply(directionfunctionprice, axis=1)
    return stock

priceshockdirection(TCS)
priceshockdirection(INFY)
priceshockdirection(NIFTY)

##Price Shock w/o volume shocks

def priceshock_wo_volshock(stock):
    
    stock["not_volshock"]  = (~(stock["volumeshock"].astype(bool))).astype(int)
    stock["priceshock_w/0_volshock"] = stock["not_volshock"] & stock["priceshock"]
    
    return stock
priceshock_wo_volshock(TCS)
priceshock_wo_volshock(INFY)
priceshock_wo_volshock(NIFTY)

