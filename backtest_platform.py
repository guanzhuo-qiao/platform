import numpy as np
import pandas as pd


class Platform:
    def __init__(self, data, factor=None):
        self.data = data
        self.factor = factor
        self.quarterly_return = None
        self.grouped_return = None

    def processor(self): # get self.quarterly_return
        pass

    def group(self, N, means):
        self.grouped_return = pd.DataFrame(columns=range(N))
        for date, factors in self.factor.iterrows():
            ticker_list = list(factors.sort_values().index)
            members = int(len(ticker_list) / N)
            gr_row = []
            for i in range(N):
                if i == N - 1:
                    grouped_tickers = ticker_list[i * members:]
                else:
                    grouped_tickers = ticker_list[i * members:(i + 1) * members]
                gr_row.append(self.quarterly_return.loc[date, grouped_tickers].mean())
            self.grouped_return.append(gr_row)




    def get_performance(self, factor=None):
        if factor:
            self.factor = factor




