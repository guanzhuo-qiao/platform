import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
from factor_generator import get_factor_table


class Platform:
    def __init__(self, monthly_return_file, quarterly_return_file, factor_name=None):

        self.monthly_return = pd.read_csv(monthly_return_file, index_col=0)
        self.quarterly_return = pd.read_csv(quarterly_return_file, index_col=0)
        self.grouped_return = None
        if factor_name:
            self.factor = get_factor_table(factor_name)

    def processor(self):

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

    def summary(self, group_num, factor_name=None):

        if factor_name:
            self.factor = get_factor_table(factor_name)
        assert len(self.quarterly_return) == len(self.factor)

        self.processor()
        self.group(group_num)
        gr_arr = np.array(self.grouped_return).T
        SP500 = np.array(self.quarterly_return.iloc[:, -1])

        # Student's t-test of mean return differential
        print("Student's t-test of mean return differential:")
        T_test_res = []
        for i in range(group_num):
            for j in range(i + 1, group_num):
                tmp_r = stats.ttest_ind(gr_arr[i], gr_arr[j], equal_var=stats.levene(gr_arr[i], gr_arr[j]).pvalue > 0.1)
                print(tmp_r)
                T_test_res.append(tmp_r)

        # Information Ratio
        print("Information Ratio:")
        info_ratio_res = []
        for r in gr_arr:
            ir = (r.mean() - SP500.mean()) / np.std(r - SP500)
            print(ir)
            info_ratio_res.append(ir)

        # Sharpe Ratio
        print("Sharpe Ratio:")
        Sharpe_ratio_res = []
        for r in gr_arr:
            sr = (r.mean() - 0.0318) / np.std(r)
            print(sr)
            Sharpe_ratio_res.append(sr)

        # Information Coefficient
        #

        fig = plt.figure(figsize=(10, 5))

        # Monotonic Test
        monotonic_graph = fig.add_subplot(1, 2, 1)
        monotonic_graph.set_title('Monotonic Test')
        for Q in gr_arr:
            # Outlier Detection and Standardization
            threshold = np.std(Q)
            Q = Q[abs(Q) < threshold]
            Q = (Q - Q.mean()) / (6 * Q.std())
            # Plot Q
            monotonic_graph.plot(Q)

        # Distribution Detection
        #

        plt.show()
        return T_test_res, info_ratio_res, Sharpe_ratio_res


bp = Platform(monthly_return_file='stock_monthly_return.csv',
              quarterly_return_file='stock_quarterly_return.csv')
bp.summary(5, "free-cash-flow-per-share")


# fig = plt.figure(figsize=(10, 5))
# # Monotonic Test
# a = [[1,2,3,4,5],
#      [6,4,7,8,9],
#      [2,3,3,4,6],
#      [3,5,6,7,8],
#      [9,0,8,7,5],
#      [6,5,6,7,9],
#      [2,3,4,5,3]]
# gr_arr = np.array(a).T
# monotonic_graph = fig.add_subplot(1, 2, 1)
# monotonic_graph.set_title('Monotonic Test')
#
# for Q in gr_arr:
#     monotonic_graph.plot(Q)
#
# plt.show()
