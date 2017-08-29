import pandas as pd
import requests
from bs4 import BeautifulSoup as BS

def get_price():
    urlfut = 'http://info512.taifex.com.tw/Future/FusaQuote_Norl.aspx?_Category=1'
    resfut = requests.get(urlfut)
    resfut.encoding = 'utf-8'
    soup = BS(resfut.text,"lxml")
    table = pd.read_html(str(soup.select('#divDG')[0]),index_col=0,header=0)[0]
    return table.filter(regex='^小臺指期0|^小臺指期1', axis=0).iloc[0:1]

def update_price(data_set):
    return pd.concat([data_set, get_price()])

# init data_set
data_set = get_price()

data_set = update_price(data_set)
