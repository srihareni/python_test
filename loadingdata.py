from nsepy import get_history
from datetime import date
import pandas as pd



TCS = get_history(symbol='TCS',
                   start=date(2015,1,1),
                   end=date(2015,12,31)) 
TCS.insert(0, 'Date',  pd.to_datetime(TCS.index,format='%Y-%m-%d') )
type(TCS.index)
type(TCS.Date)
TCS.Date.dt
TCS.to_csv('C:/Users/SRIHARINI/Desktop/dat/TCS.csv', encoding='utf-8', index=False)



INFY= get_history(symbol='INFY',
                   start=date(2015,1,1),
                   end=date(2015,12,31))

INFY
INFY.insert(0, 'Date',  pd.to_datetime(TCS.index,format='%Y-%m-%d') )
type(INFY.index)
type(INFY.Date)
INFY.Date.dt
INFY.to_csv('C:/Users/SRIHARINI/Desktop/dat/INFY.csv', encoding='utf-8', index=False)



nifty_it = get_history(symbol="NIFTY IT",
                            start=date(2015,1,1),
                            end=date(2015,12,31),
                            index=True)
nifty_it
nifty_it.insert(0, 'Date',  pd.to_datetime(nifty_it.index,format='%Y-%m-%d') )
type(nifty_it.index)
type(nifty_it.Date)
nifty_it.Date.dt
nifty_it.to_csv('C:/Users/SRIHARINI/Desktop/dat/nifty_it.csv', encoding='utf-8', index=False)
