# https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1686491104&period2=1702305859&interval=1d&events=history&includeAdjustedClose=true
#                                                       ^
#                                                       |
#                                       change that for the wanted ticker

import requests, datetime
from bs4 import BeautifulSoup
