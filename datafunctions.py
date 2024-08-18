import os
import shutil
import datetime
import subprocess
from uu import Error
import pandas as pd
from urllib.request import urlretrieve


def get_time(prompt):
    while True:
        date_str = input(prompt)
        try:
            epoch_time = int(
                datetime.datetime.strptime(date_str, "%d/%m/%Y").timestamp()
            )
            return epoch_time
        except ValueError:
            print("Invalid date format. Please try again using the format dd/mm/yyyy.")


def fetchData(ticker: str, timeStart, timeEnd):
    try:
        URL = (
            "https://query1.finance.yahoo.com/v7/finance/download/"
            + ticker
            + "?period1="
            + str(timeStart)
            + "&period2="
            + str(timeEnd)
            + "&interval=1d&events=history&includeAdjustedClose=true"
        )

        if not os.path.exists("./temp"):
            os.makedirs("./temp")

        urlretrieve(URL, f"./temp/{ticker}.csv")
        print(f"\nSUCCESS: Data fetched for {ticker}")
    except Exception as e:
        print(f"\nERROR: Could not fetch data for {ticker} - {e}")


def mergeData(csv_files):
    dataframeList = []

    for filename in csv_files:
        # Read the csv file
        dataframe = pd.read_csv(filename)

        # Extract csv file name and add it as a new column
        ticker_name = os.path.splitext(os.path.basename(filename))[0]

        # Insert the 'Ticker' column at the second position of the dataframe
        dataframe.insert(1, "Ticker", ticker_name)

        # Append the dataframe to the list
        dataframeList.append(dataframe)

    # Concatenate all dataframes in the list
    combinedDataframe = pd.concat(dataframeList)

    return combinedDataframe


def pivotData(combinedDataframe, closeType, inputFileName, dateOrder):
    if closeType.lower() == "a":
        closeType = "Adj Close"
    elif closeType.lower() == "c":
        closeType = "Close"
    else:
        print(f"Invalid closeType: {closeType}")
        return

    try:
        # Get all unique tickers from the input file
        with open(inputFileName, "r") as file:
            all_tickers = [line.strip().upper() for line in file if line.strip() != ""]

        # Create a pivot table
        pivotDataframe = combinedDataframe.pivot(index="Date", columns="Ticker", values=closeType)

        # Add missing tickers as columns with NaN values
        missing_tickers = set(all_tickers) - set(pivotDataframe.columns)
        for ticker in missing_tickers:
            pivotDataframe[ticker] = pd.NA

        # Reorder columns to match the order in the input file
        pivotDataframe = pivotDataframe.reindex(columns=all_tickers)

    except KeyError:
        print(f"Error with closeType '{closeType}'")
        return

    # Convert 'Date' column to datetime if it's not already
    pivotDataframe.index = pd.to_datetime(pivotDataframe.index)

    # Sort by date in ascending order first
    pivotDataframe = pivotDataframe.sort_index(ascending=True)

    # If descending order is requested, reverse the entire DataFrame
    if dateOrder.lower() == 'd':
        pivotDataframe = pivotDataframe.loc[pivotDataframe.index[::-1]]

    # Fill empty cells with NaN in the pivoted DataFrame
    pivotDataframe = pivotDataframe.fillna('NaN')

    # Write the pivoted dataframe to a new csv file in the directory of the input file
    inputDirectory = os.path.dirname(inputFileName)
    outputFileName = "{}-{}-output.csv".format(
        os.path.splitext(os.path.basename(inputFileName))[0],
        closeType.lower().replace(" ", "-"),
    )
    outputPath = os.path.join(inputDirectory, outputFileName)
    pivotDataframe.to_csv(outputPath)

    print("\nOpening Excel...")
    subprocess.Popen(["start", "excel", "/x", "/r", outputPath], shell=True)
