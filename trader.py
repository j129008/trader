import pandas as pd
import requests
from bs4 import BeautifulSoup as BS
from time import sleep
import os
from threading import Thread
from datetime import datetime, time
import pickle

class future(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.price_set = self.get_price()

    def get_price(self):
        urlfut = 'http://info512.taifex.com.tw/Future/FusaQuote_Norl.aspx?_Category=1'
        resfut = requests.get(urlfut)
        resfut.encoding = 'utf-8'
        soup = BS(resfut.text,"lxml")
        table = pd.read_html(str(soup.select('#divDG')[0]),index_col=0,header=0)[0]
        price = table.filter(regex='^小臺指期0|^小臺指期1', axis=0).iloc[0:1]
        return price

    def update_price(self):
        self.price_set = pd.concat([self.price_set, self.get_price()])

    def run(self):
        start_time = time( 8, 44, 00 )
        end_time = time( 13, 45, 30 )
        print('market open: ' + datetime.now().isoformat())
        while start_time < datetime.now().time() < end_time:
            self.update_price()
            sleep(15)
            pickle.dump(self.price_set, open('/home/vodo/trader/history/' + datetime.strftime(datetime.now(),"%Y_%m_%d") + '.pkl', 'wb'))
            trade_time = datetime.now().time()
            print('trade time: ' + trade_time.isoformat())
        end_time = datetime.now().time()
        print('market close: ' + end_time.isoformat())
        return 0

if __name__ == "__main__":
    fut = future()
    fut.start()
    fut.join()
    print('proc exit: ' + datetime.now().isoformat())
