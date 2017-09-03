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
        time_group = []
        for time in set(time_list):
            time_group.append( [time] * time_cnt[time] )

        for i in range(len(time_group)):
            self.time_split(time_group[i])
        new_time_list = []
        for group in time_group:
            new_time_list += group
        self.data['成交時間'] = sorted(new_time_list)

if __name__ == '__main__':
    path_list = glob('./history/*.csv')
    fut_list = sorted([fut_load(path) for path in path_list], key=lambda x:x.trade_date)
