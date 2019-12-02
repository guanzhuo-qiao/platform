import pandas as pd
import numpy as np
from datetime import datetime

file = 'FDA_calender.csv'

df = pd.read_csv(file, index_col=0)
sample_col = ["Ticker", "Stage", "Catalyst-date"]

# What we need to generate the factor table
res = pd.read_csv('stock_quarterly_return.csv', index_col=0)
res.loc[:, :] = 0
col = res.columns.values
df_stage = df.loc[:, sample_col]

stage_label = {'blaFiling': 4,
               'ndaFiling': 4,
               'pdufa': 5,
               'pdufaPriortyReview': 5,
               'phase1': 1,
               'phase1.5': 1,
               'phase1b': 1,
               'phase2': 2,
               'phase23': 3,
               'phase2a': 2,
               'phase2b': 2,
               'phase3': 3,
               'approved': 6,
               'crl': -6}

discount = [1, 0.2, 0.35, 0.5, 0.6, 0.8, 1]

# Use the stage level to weight the stage score
temp_list = []
for t in df_stage.Stage:
    if t in stage_label.keys():
        if t == 'crl':
            temp_list.append(stage_label['crl'])
        else:
            temp_list.append(discount[stage_label[t]] * stage_label[t])
    else:
        temp_list.append(np.nan)
df_stage['stage_score'] = temp_list


def str2time4stage(x):
    return datetime.strptime(x, '%m/%d/%Y')


def str2time4res(x):
    return datetime.strptime(x, '%Y-%m-%d')


index = res.index
for i, event in df_stage.iterrows():
    if event['Ticker'] in col:
        tmp = ''
        for date in index:
            if str2time4stage(event['Catalyst-date']) < str2time4res(date):
                tmp = date
                break
        res.loc[tmp, event['Ticker']] = event['stage_score']

res = res.fillna(0)
print(res)
res.to_csv('FDA_factor.csv')







