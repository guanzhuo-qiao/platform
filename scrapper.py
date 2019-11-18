from bs4 import BeautifulSoup
from urllib import request
import urllib
import requests
import pandas as pd
import os

os.chdir(r"D:\Grad3\670\Assignment\platform")
stock_list = pd.read_csv(r"MSCI_US_IMI_HC_benchmark_info_js2(1).csv")
for row in range(len(stock_list)):
    t = stock_list.iloc[row,4]
    if " Inc." in t:
        t = t[:t.find(" Inc")]
    if " Corp." in t:
        t = t[:t.find(" Corp")]
    if " Co." in t:
        t = t[:t.find(" Co.")]
    if "&" in t:
        t = t.replace("&","")
    if "and" in t:
        t = t.replace("and","")
    if "plc" in t:
        t = t[:t.find(" plc")]
    if "Ltd." in t:
        t = t[:t.find(" Ltd.")]
    if "Class" in t:
        t = t[:t.find(" Class")]
    if "Cos" in t:
        t = t[:t.find(" Cos")]
    if "NV" in t:
        t = t[:t.find(" NV")]
    t = t.lower()
    t = "-".join(t.split(" "))
    stock_list.iloc[row, 4] = t
stock_list.to_csv("stock_list.csv")
os.chdir(r"D:\Grad3\670\Assignment\platform\factor")
for row in range(len(stock_list)):
    symbol = stock_list.iloc[row,0]
    company_name = stock_list.iloc[row, 4]
    url = f"https://www.macrotrends.net/stocks/charts/{symbol}/{company_name}/financial-ratios?freq=Q"
    res = request.urlopen(url)
    if "freq=Q" not in res.url:
        url = res.url+"?freq=Q"
        res = request.urlopen(url)
    print(url)
    soup = BeautifulSoup(res)
    num = soup.find_all("body")
    text = num[0].text
    begin_ind = text.find("var originalData")
    end_ind = text[begin_ind:].find("var source")
    text = text[begin_ind:begin_ind+end_ind]
    text = text[text.find("["):text.find("]")+1]
    data = text.split(",")
    table = pd.DataFrame()
    for ele in data:
        if " s:" in ele:
            table_ind = ele.split("'")[1]
        elif "\"20" in ele:
            number = float(ele.split(":")[1].strip("}\"}]")) if ele.split(":")[1].strip("}\"}]") != "" else None
            table_column = ele.split(":")[0].strip("\"")
            table.loc[table_ind,table_column] = number
    table.to_csv(f"{symbol}_financial_statement.csv")





