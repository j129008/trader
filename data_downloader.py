from datetime import date, timedelta
import urllib.request
from pathlib import Path

class fut_data:
    def __init__(self, data_location):
        self.url = 'http://www.taifex.com.tw/DailyDownload/DailyDownloadCSV/Daily_'
        self.today = date.today()
        self.folder = data_location
    def past_day(self, day):
        past_day = self.today - timedelta(days=day)
        file_name = past_day.strftime('%Y_%0m_%0d') + '.zip'
        file_path = Path(self.folder + file_name)
        if not file_path.exists():
            if past_day.isoweekday() not in [6, 7]:
                urllib.request.urlretrieve(self.url + file_name, self.folder + file_name)
                print('save ' + file_name + ' success')
            else:
                print('is weekend')
        else:
            print('file exist')

if __name__ == '__main__':
    fut = fut_data('/home/vodo/trader/history/')
    for i in range(30):
        fut.past_day(i)
