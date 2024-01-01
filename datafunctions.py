import os
import shutil
import pandas as pd
from urllib.request import urlretrieve
# from colorama import Fore, Style

def fetchData(ticker: str, timeStart, timeEnd):
    try:
        URL = "https://query1.finance.yahoo.com/v7/finance/download/" + ticker + "?period1=" + str(timeStart) + "&period2=" + str(timeEnd) + "&interval=1d&events=history&includeAdjustedClose=true"
        # print(Fore.BLUE + "Fetching " + Style.RESET_ALL + ticker + " from " + URL + "\n")

        if not os.path.exists('./temp'):
            os.makedirs('./temp')

        urlretrieve(URL, "./temp/" + ticker + ".csv")
        # print(Fore.GREEN + "Success" + Style.RESET_ALL + " Fetching " + ticker + "\n" )
        print("SUCCESS" + " Fetching " + ticker + "\n" )
    except:
        # print(Fore.RED + "Error" + Style.RESET_ALL + " Fetching Ticker \'" + ticker + "\'\n")
        print("ERROR" + " Fetching Ticker \'" + ticker + "\'\n")

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

def pivotData(combinedDataframe, closeType):
    if closeType == "Adj":
        closeType = "Adj Close"
    elif closeType == "Close":
        closeType = "Close"
    try:
        # Pivot the DataFrame so 'Ticker' becomes the columns and closeType becomes the row corresponding to the ticker
        pivotDataframe = combinedDataframe.pivot(index='Date', columns='Ticker', values=closeType)
    except:
        # print(Fore.RED + "Error" + Style.RESET_ALL + " with closeType \'" + closeType + "\'")
        print("Error" + " with closeType \'" + closeType + "\'")
        shutil.rmtree('./temp')
        exit()
    # Write the pivoted dataframe to a new csv file in /out directory
    pivotDataframe.to_csv('./out.csv')
