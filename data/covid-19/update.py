import urllib.request
import datetime

dt = datetime.datetime

import numpy as np
import pandas as pd

BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"

urls = {
	'cases': BASE_URL + "time_series_covid19_confirmed_global.csv",
	'deaths': BASE_URL + "time_series_covid19_deaths_global.csv",
	'recovered': BASE_URL + "time_series_covid19_recovered_global.csv"
}


for variable in ['cases', 'deaths', 'recovered']:
	
	raw = pd.read_csv(urls[variable], index_col=[0,1], na_filter=False).groupby("Country/Region").sum()
	index = list(map(lambda s: dt(int(s.split('/')[2])+2000, int(s.split('/')[0]), int(s.split('/')[1])), raw.columns[2:]))
	df = pd.DataFrame(raw[raw.columns[2:]].T).reset_index(drop=True)
	df['date'] = index
	df.set_index('date', inplace=True)
	print(df)
	df.to_json(variable+'.json')
