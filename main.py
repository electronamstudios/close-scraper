import os
import glob
import time
import shutil
import datetime
import datafunctions as df
from colorama import Fore, Style

# ------------------------------------ Setup

timeStart = int(time.mktime(datetime.datetime.strptime(input("Starting Date (%d/%m/%y): "), "%d/%m/%Y").timetuple()))
timeEnd = int(time.mktime(datetime.datetime.strptime(input("Ending Date (%d/%m/%y): "), "%d/%m/%Y").timetuple()))

tickerCount = int(input("\nHow many tickers do you want: "))
tickerList = []

for i in range(tickerCount):
    ticker = input("Ticker: ").upper()
    tickerList.append(ticker)

print("\nGenerating URLs for " + str(tickerList) + "\n")
for i in range(tickerCount):
    df.fetchData(tickerList[i], timeStart, timeEnd)

# ------------------------------------ Merge Data

# Get the csv files in the /temp directory
csv_files = glob.glob('./temp/*.csv')

combinedDataframe = df.mergeData(csv_files)

closeType = input("Enter 'Adj' or 'Close' to choose the type of value you want to see: ")

print("\n" + Fore.BLUE + "Merging" + Style.RESET_ALL + " .csv files...")

df.pivotData(combinedDataframe, closeType)

if os.path.exists('./temp'):
    shutil.rmtree('./temp')

print("\n" + Fore.GREEN + "Finished!" + Style.RESET_ALL + " Output saved to ./out.csv \n")
