from os import path, makedirs 
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
        print(f"SUCCESS: Data fetched for {ticker}\n")
    except Exception as e:
        print(f"ERROR: Could not fetch data for {ticker} - {e}\n")


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

    # Convert 'Date' column to datetime if it's not already
    combinedDataframe['Date'] = pd.to_datetime(combinedDataframe['Date'])

    # Sort by date according to dateOrder
    if dateOrder.lower() == 'a':
        combinedDataframe = combinedDataframe.sort_values(by='Date', ascending=True)
    elif dateOrder.lower() == 'd':
        combinedDataframe = combinedDataframe.sort_values(by='Date', ascending=False)
    else:
        print(f"Invalid dateOrder: {dateOrder}")
        return

    # Pivot the DataFrame so 'Ticker' becomes the columns and closeType becomes the row corresponding to the ticker
    try:
        pivotDataframe = combinedDataframe.pivot(index="Date", columns="Ticker", values=closeType)
    except KeyError:
        print(f"Error with closeType '{closeType}'")
        return

    # Write the pivoted dataframe to a new csv file in the directory of the input file
    inputDirectory = path.dirname(inputFileName)
    outputFileName = "{}-{}-output.csv".format(
        path.splitext(path.basename(inputFileName))[0],
        closeType.lower().replace(" ", "-"),
    )
    outputPath = path.join(inputDirectory, outputFileName)
    pivotDataframe.to_csv(outputPath)

    print("\nOpening Excel...")
    subprocess.Popen(["start", "excel", "/x", "/r", outputPath], shell=True)
