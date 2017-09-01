from datetime import datetime
import urllib.request

today = str( datetime.strftime(datetime.now(),"%Y_%2m_%2d") )
url = 'http://www.taifex.com.tw/DailyDownload/DailyDownloadCSV/Daily_'+ today +'.zip'
urllib.request.urlretrieve(url, '/home/vodo/trader/history/' + today + '.zip')
