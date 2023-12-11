## a program that takes tickers and returns their price from a certain time range

the new finance page has a download button so i wonder if i could just convert a date into unix timecode and then inject that into the url
then download that delete the useless stuff and combine it with other stuff that was taken

https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1686491104&period2=1702305859&interval=1d&events=history&includeAdjustedClose=true

take that and change the `AAPL` to whatever the user selects

prob a cli that says what tickers do you want
-t for tickers
-d for date