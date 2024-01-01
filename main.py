import os
import glob
import time
import shutil
import datafunctions as df
from tkinter import filedialog
# from colorama import Fore, Style

# ------------------------------------ Setup

timeStart = df.get_time("Starting Date (dd/mm/yyyy): ")
while True:
    timeEnd = df.get_time("Ending Date (dd/mm/yyyy): ")
    if timeEnd > timeStart:
        break
    print("Ending date must be after starting date. Please try again.")

print("\nSelect tab-delimited text file with tickers")

ticker_filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
with open(ticker_filename, 'r') as file:
    tickerList = [line.strip().upper() for line in file if line.strip() != '']

print("\nGenerating URLs for " + str(len(tickerList)) + " tickers.\n")
for index, ticker in enumerate(tickerList, start=1):
    print(f"Fetching data for ticker {index} of {len(tickerList)}: {ticker}")
    df.fetchData(ticker, timeStart, timeEnd)

# ------------------------------------ Merge Data

# Get the csv files in the /temp directory
csv_files = glob.glob('./temp/*.csv')

combinedDataframe = df.mergeData(csv_files)

closeType = input("Enter 'a' or 'c' to choose adjusted close or close: ")

# print("\n" + Fore.BLUE + "Merging" + Style.RESET_ALL + " .csv files...")
print("\n" + "Merging" + " .csv files...")

df.pivotData(combinedDataframe, closeType)

if os.path.exists('./temp'):
    shutil.rmtree('./temp')

# print("\n" + Fore.GREEN + "Finished!" + Style.RESET_ALL + " Output saved to ./out.csv \n")
print("\n" + "Finished!")
