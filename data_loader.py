import pandas as pd
from collections import Counter
from pathlib import Path
import re
from glob import glob

class fut_load:
    def __init__(self, data_path):
        file_name = Path(data_path).name
        self.trade_date = int(re.sub('[A-z_\.]', '', file_name))
        self.data = pd.read_csv(data_path, encoding='big5')
        self.data['商品代號'] = self.data['商品代號'].str.strip()
        self.data = self.data.loc[self.data['商品代號'] == 'MTX']
        self.data = self.data.loc[self.data['成交日期'] == self.trade_date]
        self.data = self.data.loc[self.data['成交價格'] > 0]
        self.data = self.data.loc[self.data['成交時間'] >= 84500]
        self.set_time()

    def time_split(self, time_list):
        if len(time_list) == 1:
            return time_list
        delta = 1/len(time_list)
        for i in range(len(time_list)):
            time_list[i] += i*delta
        return time_list

    def set_time(self):
        time_list = [ ele for ele in self.data['成交時間'] ]
        time_cnt = Counter(time_list)
        new_time_list = []
        for time in set(time_list):
            new_time_list.append( [time] * time_cnt[time] )

        for i in range(len(new_time_list)):
            self.time_split(new_time_list[i])
        new_time_list2 = []
        for ele in new_time_list:
            new_time_list2 += ele
        new_time_list2 = sorted(new_time_list2)
        self.data['成交時間'] = new_time_list2

if __name__ == '__main__':
    path_list = glob('./history/*.csv')
    fut_list = sorted([fut_load(path) for path in path_list], key=lambda x:x.trade_date)
