import pandas as pd
import os
def get_factor_table(keyword):
    stock_data = pd.read_csv("stock_quarterly_return.csv",index_col = 0)
    time_index = stock_data.index
    stock_index = stock_data.columns

    factor_data = pd.DataFrame(columns=stock_index,index=time_index)
    os.chdir(os.getcwd()+r"\factor")
    file_list = os.listdir()
    for file_name in file_list:
        file_content = pd.read_csv(file_name,index_col=0)
        symbol = file_name.split("_")[0]
        try:
            factor_data.loc[:,symbol] = file_content.loc[keyword,:][time_index]
        except KeyError:
            pass
    return factor_data

if __name__=="__main__":
    print(get_factor_table("free-cash-flow-per-share"))

