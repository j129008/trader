import pandas as pd
import requests
from bs4 import BeautifulSoup as BS

class future:
    def __init__(self):
        self.price_set = self.get_price()

    def get_price(self):
        urlfut = 'http://info512.taifex.com.tw/Future/FusaQuote_Norl.aspx?_Category=1'
        resfut = requests.get(urlfut)
        resfut.encoding = 'utf-8'
        soup = BS(resfut.text,"lxml")
        table = pd.read_html(str(soup.select('#divDG')[0]),index_col=0,header=0)[0]
        return table.filter(regex='^小臺指期0|^小臺指期1', axis=0).iloc[0:1]

    def update_price(self):
        self.price_set = pd.concat([self.price_set, self.get_price()])

