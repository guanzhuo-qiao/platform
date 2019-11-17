import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Platform:
    def __init__(self, monthly_return_file, quarterly_return_file, factor=None):

        self.monthly_return = pd.read_csv(monthly_return_file, index_col=0)
        self.quarterly_return = pd.read_csv(quarterly_return_file, index_col=0)
        self.factor = factor
        self.grouped_return = None
        self.init_processor()

    def init_processor(self):

        self.monthly_return.fillna(0)
        self.quarterly_return.fillna(0)
        self.factor.fillna(0)

    def group(self, N, ascending=True):

        self.grouped_return = pd.DataFrame(columns=range(N))
        for date, factors in self.factor.iterrows():
            ticker_list = list(factors.sort_values(ascending=ascending).index)
            members = int(len(ticker_list) / N)
            gr_row = []
            for i in range(N):
                if i == N - 1:
                    grouped_tickers = ticker_list[i * members:]
                else:
                    grouped_tickers = ticker_list[i * members:(i + 1) * members]
                gr_row.append(self.quarterly_return.loc[date, grouped_tickers].mean())
            self.grouped_return = self.grouped_return.append([gr_row], ignore_index=True)

    def summary(self, factor=None):

        if factor:
            self.factor = factor
        assert len(self.quarterly_return) == len(self.factor)




bp = Platform(monthly_return_file='stock_monthly_return.csv',
              quarterly_return_file='')
bp.summary()

