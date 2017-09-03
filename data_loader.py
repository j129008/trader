import pandas as pd
from collections import Counter

def time_split(time_list):
    if len(time_list) == 1:
        return time_list
    delta = 1/len(time_list)
    for i in range(len(time_list)):
        time_list[i] += i*delta
    return time_list

def set_time(data):
    time_list = [ ele for ele in data['成交時間'] ]
    time_cnt = Counter(time_list)
    new_time_list = []
    for time in set(time_list):
        new_time_list.append( [time] * time_cnt[time] )

    for i in range(len(new_time_list)):
        time_split(new_time_list[i])
    new_time_list2 = []
    for ele in new_time_list:
        new_time_list2 += ele
    new_time_list2 = sorted(new_time_list2)
    data['成交時間'] = new_time_list2

data = pd.read_csv('./history/Daily_2017_08_07.csv', encoding='big5')
data['商品代號'] = data['商品代號'].str.strip()
data = data.loc[data['商品代號'] == 'MTX']
data = data.loc[ data['成交日期'] == 20170807 ]
data = data.loc[data['成交價格'] > 0]
set_time(data)
