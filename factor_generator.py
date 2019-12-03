import pandas as pd
import os


def get_factor_table(keyword,file_path):
    """
    fetch a single factor

    :param keyword: the factor name
    :param file_path: the file's name to which the factor you mentioned belongs to.
                      i.e. get_factor_table("free-cash-flow-per-share","factor_financial_ratios")
    :return: DataFrame with 0
    """
    if keyword=="fda" and file_path=="platform":
        factor_data = pd.read_csv("FDA_factor.csv",index_col=0)
        factor_data = factor_data.rank(pct=True,ascending=True,axis=1)
        return factor_data

    stock_data = pd.read_csv("stock_quarterly_return.csv",index_col = 0)
    time_index = stock_data.index
    stock_index = stock_data.columns

    factor_data = pd.DataFrame(columns=stock_index,index=time_index)
    os.chdir(os.getcwd()+f"/{file_path}")
    file_list = os.listdir()
    for file_name in file_list:
        file_content = pd.read_csv(file_name,index_col=0)
        symbol = file_name.split("_")[0]
        try:
            factor_data.loc[:,symbol] = file_content.loc[keyword,:][time_index]
        except KeyError:
            pass
    path = os.getcwd()
    path = "/".join(path.split("/")[:-1])   # Here!!!
    os.chdir(path)
    factor_data = factor_data.fillna(0)
    factor_data = factor_data.rank(pct=True, ascending=True, axis=1)
    return factor_data


def factor_function(func,factor_dict):
    """
    fetch and combine the factors

    :param func: the function object which operate the dataframe in terms of factor operations. The function
    should use the keys that passed. Like if defined as f(x,y), the dict should use "x" and "y" to be the dict keys.
    :param factor_dict: a dictionary that indicate the relationship between function and factor symbols.
                        i.e.  dictionary = {"x":("free-cash-flow-per-share","factor_financial_ratios"),
                                            "y":("net-income-loss","factor_cash_flow_statement")}
    :return: a combined DataFrame
    """
    inner_dic = {}
    for key,x in factor_dict.items():
        inner_dic[key] = get_factor_table(*x)
    return func(**inner_dic)

if __name__=="__main__":
    print(get_factor_table("fda", "platform"))
    print(get_factor_table("free-cash-flow-per-share","factor_financial_ratios"))
    print(get_factor_table("net-income-loss","factor_cash_flow_statement"))
    dictionary = {"x":("free-cash-flow-per-share","factor_financial_ratios"),
                  "y":("net-income-loss","factor_cash_flow_statement")}
    def f(x,y):
        return x+y
    print(factor_function(f,dictionary))

