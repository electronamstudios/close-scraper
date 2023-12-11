# https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1686491104&period2=1702305859&interval=1d&events=history&includeAdjustedClose=true
#                                                       ^
#                                                       |
#                                       change that for the wanted ticker

import requests, datetime, urllib
from bs4 import BeautifulSoup

timeStart = "" # unix timecode
timeEnd = "" # unix timecode

tickerCount = int(input("How many tickers do you want: "))
tickerList = []

for i in range(tickerCount):
    ticker = input("Enter ticker name: ").upper()
    tickerList.append(ticker)

print(tickerList)
