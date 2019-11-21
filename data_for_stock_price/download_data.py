#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 14:25:27 2019

@author: shensheng
"""

import pandas as pd
from pandas_datareader import data as pdrd
from datetime import datetime

stock_list = pd.read_csv("MSCI_US_IMI_HC_benchmark_info_js2.csv")

symbol = stock_list['Symbol'].tolist()
symbol.append('^GSPC')

data = pdrd.get_data_yahoo(symbol,'01/01/2009',interval='m')
stock_price = data.iloc[0:130,1930:]
stock_price.to_csv('combined equity data.csv')


equitydata = pd.DataFrame()
for stock in symbol:
    equitylist = pdrd.get_data_yahoo(stock,'01/01/2009',interval='m').iloc[:,5]
    equitydata = pd.concat([equitydata, equitylist], axis=1)

equitydata = equitydata.iloc[0:130,:]
equitydata.columns = symbol
equitydata.to_csv('combined_stock_price.csv')

monthly_return = equitydata.pct_change()
# remote the first line
monthly_return = monthly_return.iloc[1:, :]

monthly_return.to_csv('stock_monthly_return.csv')

#quarterly return
quarterly_return = pd.DataFrame()
index = list(range(0, len(equitydata), 3))
q_data = equitydata.iloc[index]

res = (q_data - q_data.shift(1)) / q_data.shift(1)

res  = res.iloc[1:,:]


res.index = res.index-datetime.timedelta(days=1)#convert datetime into quarterly (minus 1)
res.to_csv('stock_quarterly_return.csv')


