import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import datetime
import yfinance as yf

api_key = '7NQ5H1FQHLLH7JFC'

ts = TimeSeries(key=api_key, output_format='pandas')

try:
	symbol = 'MSFT'
	date_time = 'No date...'
	data, meta_data = ts.get_intraday(symbol=symbol, interval = '60min', outputsize = 'full')
	close_data = data['4. close']
	open_data = data['1. open']
	date_time = datetime.datetime.now()
	initial_price = open_data[-1]
	final_price = close_data[-1]
	value_changes = final_price - initial_price
	percent_change = (final_price - initial_price)/initial_price*100

	tickerdata = yf.Ticker(symbol)
	tickerinfo = tickerdata.info
	company_name = tickerinfo['shortName']

	if value_changes > 0:
		output = str(initial_price) +' +'+ str(value_changes) + ' +' + str(percent_change) + '%'
	if value_changes < 0:
		output = str(initial_price) +' '+ str(value_changes) + ' ' + str(percent_change) + '%'
	print(company_name)
	print(date_time)
	print(output)
           
except:
	print("No such symbol..")


 # pytz, numpy, six, python-dateutil, pandas, idna, chardet, urllib3, certifi, requests, multitasking, yfinance