import os
import glob
import time
import shutil
import datetime
import datafunctions as df
from tkinter import filedialog
from colorama import Fore, Style

# ------------------------------------ Setup

timeStart = int(time.mktime(datetime.datetime.strptime(input("Starting Date (%d/%m/%y): "), "%d/%m/%Y").timetuple()))
timeEnd = int(time.mktime(datetime.datetime.strptime(input("Ending Date (%d/%m/%y): "), "%d/%m/%Y").timetuple()))

print("\nSelect tab-delimited text file with tickers")

ticker_filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
with open(ticker_filename, 'r') as file:
    tickerList = [line.strip().upper() for line in file if line.strip() != '']

print("\nGenerating URLs for " + str(tickerList) + "\n")
for ticker in tickerList:
    df.fetchData(ticker, timeStart, timeEnd)

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

os.system('start excel /x /r ./out.csv')
