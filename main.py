import os
import glob
import time
import shutil
import datetime
import pandas as pd
from colorama import Fore, Style
from urllib.request import urlretrieve

# ------------------------------------ Setup

timeStart = int(time.mktime(datetime.datetime.strptime(input("Starting Date (%d/%m/%y): "), "%d/%m/%Y").timetuple()))
timeEnd = int(time.mktime(datetime.datetime.strptime(input("Ending Date (%d/%m/%y): "), "%d/%m/%Y").timetuple()))

tickerCount = int(input("\nHow many tickers do you want: "))
tickerList = []

for i in range(tickerCount):
    ticker = input("Ticker: ").upper()
    tickerList.append(ticker)

print("\nGenerating URLs for " + str(tickerList) + "\n")

# ------------------------------------ Fetch Data

def fetchData(ticker, timeStart, timeEnd):
    try:
        URL = "https://query1.finance.yahoo.com/v7/finance/download/" + ticker + "?period1=" + str(timeStart) + "&period2=" + str(timeEnd) + "&interval=1d&events=history&includeAdjustedClose=true"
        print(Fore.BLUE + "Fetching " + Style.RESET_ALL + ticker + " from " + URL + "\n")

        if not os.path.exists('./temp'):
            os.makedirs('./temp')

        urlretrieve(URL, "./temp/" + ticker + ".csv")
        print(Fore.GREEN + "Success" + Style.RESET_ALL + " Fetching " + ticker + "\n" )
    except:
        print(Fore.RED + "Error" + Style.RESET_ALL + " Fetching Ticker \'" + ticker + "\'\n")

def mergeData(csv_files):
    dataframeList = []

    for filename in csv_files:
        # Read the csv file
        dataframe = pd.read_csv(filename)

        # Extract csv file name and add it as a new column
        ticker_name = os.path.splitext(os.path.basename(filename))[0]
        
        # Insert the 'Ticker' column at the second position of the dataframe
        dataframe.insert(1, 'Ticker', ticker_name)

        # Append the dataframe to the list
        dataframeList.append(dataframe)

    # Concatenate all dataframes in the list
    combinedDataframe = pd.concat(dataframeList)

    return combinedDataframe

def pivotData(combinedDataframe, valueType):
    if valueType == "Adj":
        valueType = "Adj Close"
    elif valueType == "Close":
        valueType = "Close"
    
    try:
        # Pivot the DataFrame so 'Ticker' becomes the columns and valueType becomes the row corresponding to the ticker
        pivotDataframe = combinedDataframe.pivot(index='Date', columns='Ticker', values=valueType)
    except:
        print(Fore.RED + "Error" + Style.RESET_ALL + " with valueType \'" + valueType + "\'")
        shutil.rmtree('./temp')
        exit()

    # Write the pivoted dataframe to a new csv file in /out directory
    pivotDataframe.to_csv('./out.csv')

for i in range(tickerCount):
    fetchData(tickerList[i], timeStart, timeEnd)

# ------------------------------------ Merge Data

# Get the csv files in the /temp directory
csv_files = glob.glob('./temp/*.csv')

combinedDataframe = mergeData(csv_files)

valueType = input("Enter 'Adj' or 'Close' to choose the type of value you want to see: ")

print("\n" + Fore.BLUE + "Merging" + Style.RESET_ALL + " .csv files...")

pivotData(combinedDataframe, valueType)

if os.path.exists('./temp'):
    shutil.rmtree('./temp')

print("\n" + Fore.GREEN + "Finished!" + Style.RESET_ALL + " Output saved to ./out.csv \n")
