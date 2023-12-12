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

for i in range(len(tickerList)):
    try:
        URL = "https://query1.finance.yahoo.com/v7/finance/download/" + tickerList[i] + "?period1=" + str(timeStart) + "&period2=" + str(timeEnd) + "&interval=1d&events=history&includeAdjustedClose=true"
        print(Fore.BLUE + "Fetching " + Style.RESET_ALL + tickerList[i] + " from " + URL + "\n")

        if not os.path.exists('./temp'):
            os.makedirs('./temp')

        urlretrieve(URL, "./temp/" + tickerList[i] + ".csv")
        print(Fore.GREEN + "Success" + Style.RESET_ALL + " Fetching " + tickerList[i] + "\n" )
    except:
        print(Fore.RED + "Error" + Style.RESET_ALL + " Fetching Ticker \'" + tickerList[i] + "\'\n")

print(Fore.BLUE + "Merging" + Style.RESET_ALL + " .csv files...")

# ------------------------------------ Merge Data

# Get the csv files in the /temp directory
csv_files = glob.glob('./temp/*.csv')

# List to store dataframes
df_list = []

# Loop through files
for filename in csv_files:
    # Read the csv file
    df = pd.read_csv(filename)

    # Select only the "Date", "Adj Close", and "Close" columns
    df = df[["Date", "Adj Close", "Close"]]

    # Extract csv file name and add it as a new column
    ticker_name = os.path.splitext(os.path.basename(filename))[0]
    
    # Insert the 'Ticker' column at the second position of the dataframe
    df.insert(1, 'Ticker', ticker_name)

    # Append the dataframe to the list
    df_list.append(df)

# Concatenate all dataframes in the list
combined_df = pd.concat(df_list)

# Write the concatenated dataframe to a new csv file in /out directory
combined_df.to_csv('./out.csv', index=False)

if os.path.exists('./temp'):
    shutil.rmtree('./temp')

print(Fore.GREEN + "Finished!" + Style.RESET_ALL + " Output saved to ./out.csv")