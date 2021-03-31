from binance_client import client
import pandas as pd


columns = ['Date','Open','High','Low','Close' ,'Volume','IGNORE','Quote_Volume','Trades_Count','BUY_VOL','BUY_VOL_VAL','x']


def get_klines(pair, interval, depth):
	data = client.get_historical_klines(pair, interval, depth)
	df = pd.DataFrame(data)
	if not df.empty:
		df.columns = columns
		df["Volume"] = df["Quote_Volume"]
		for x in range(6, 12):
			del df[columns[x]]
		df['Date'] =  pd.to_datetime(df['Date'],unit='ms')
		df = df.set_index('Date')
		df["Close"] = pd.to_numeric(df["Close"])
		df["Open"] = pd.to_numeric(df["Open"])
		df["High"] = pd.to_numeric(df["High"])
		df["Low"] = pd.to_numeric(df["Low"])
	return df
