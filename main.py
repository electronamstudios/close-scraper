import os
import time
import datetime
from urllib.request import urlretrieve

timeStart = int(time.mktime(datetime.datetime.strptime(input("Starting Date (%d/%m/%y): "), "%d/%m/%Y").timetuple()))
timeEnd = int(time.mktime(datetime.datetime.strptime(input("Ending Date (%d/%m/%y): "), "%d/%m/%Y").timetuple()))

tickerCount = int(input("\nHow many tickers do you want: "))
tickerList = []

print("\n(uppercase not required)")
for i in range(tickerCount):
    ticker = input("Enter ticker name: ").upper()
    tickerList.append(ticker)

print("\nGenerating URLs for " + str(tickerList) + "\n")

list(tickerList)

for i in range(len(tickerList)):
    try:
        URL = "https://query1.finance.yahoo.com/v7/finance/download/" + tickerList[i] + "?period1=" + str(timeStart) + "&period2=" + str(timeEnd) + "&interval=1d&events=history&includeAdjustedClose=true"
        print("Fetching " + tickerList[i] + " from " + URL + "\n")

        if not os.path.exists('./temp'):
            os.makedirs('./temp')

        urlretrieve(URL, "./temp/" + tickerList[i] + ".csv")
    except:
        print("Error Fetching Ticker \'" + tickerList[i] + "\'\n")