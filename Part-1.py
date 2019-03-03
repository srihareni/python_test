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

