import numpy as np
import pandas as pd


class Platform:
    def __init__(self, data_file, factor=None):
        self.data = pd.read_csv(data_file, index_col=0)
        self.factor = factor
        self.quarterly_return = None
        self.grouped_return = None

    def init_processor(self, num_of_month):  # get self.quarterly_return


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

    def get_performance(self, factor=None):
        if factor:
            self.factor = factor
        assert len(self.quarterly_return) == len(self.factor)


mass = pd.read_csv('stock_monthly_return.csv', index_col=0)
print(mass)
