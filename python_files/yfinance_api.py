import yfinance as yf
from pandas_datareader import data as pdr


def getHistory(symbols:str,start:str="",end:str=""):

    yf.pdr_override()
    if start and not end:
            return pdr.DataReader(symbols, data_source='yahoo',start=start)
    elif start and end:
            return pdr.DataReader(symbols, data_source='yahoo',start=start,end=end)

    return pdr.DataReader(symbols, data_source='yahoo')
    
   
def getInfo(symbol:str):
        return yf.Ticker(symbol).info


    # data=yf.download(
    #     tickers=symbols,
    #     period=period,
    #     interval=interval,
    #     auto_adjust = True,
    #     threads = True,
    # )
    