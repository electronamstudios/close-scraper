# https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1686491104&period2=1702305859&interval=1d&events=history&includeAdjustedClose=true
#                                                       ^
#                                                       |
#                                       change that for the wanted ticker

import requests,time,datetime,urllib

timeStart = int(time.mktime(datetime.datetime.strptime(input("Starting Date (%d/%m/%y): "), "%d/%m/%Y").timetuple()))
timeEnd = int(time.mktime(datetime.datetime.strptime(input("Ending Date (%d/%m/%y): "), "%d/%m/%Y").timetuple()))

tickerCount = int(input("How many tickers do you want: "))
tickerList = []

print("\n(uppercase not required)")
for i in range(tickerCount):
    ticker = input("Enter ticker name: ").upper()
    tickerList.append(ticker)

print("\nGenerating URLs for " + str(tickerList) + "\n")

for i in range(len(tickerList)):
    url = "https://query1.finance.yahoo.com/v7/finance/download/" + tickerList[i] + "?period1=" + str(timeStart) + "&period2=" + str(timeEnd) + "&interval=1d&events=history&includeAdjustedClose=true"
    print(url)