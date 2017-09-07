from datetime import date, timedelta
import urllib3
from pathlib import Path
from zipfile import ZipFile, is_zipfile
import os

class fut_data:
    def __init__(self, data_location):
        self.url = 'http://www.taifex.com.tw/DailyDownload/DailyDownloadCSV/Daily_'
        self.today = date.today()
        self.folder = data_location
    def past_day(self, day):
        past_day = self.today - timedelta(days=day)
        file_date = past_day.strftime('%Y_%0m_%0d')
        file_name = file_date + '.zip'
        file_path = Path(self.folder + file_name)
        csv_path = Path(self.folder + 'Daily_' + file_date + '.csv')
        if csv_path.exists(): return 'csv exist'
        if past_day.isoweekday() in [6, 7]: return 'is weekend'
        http = urllib3.PoolManager()
        r = http.request('GET', self.url + file_name)
        if r.status == 200:
            fout = open(str(file_path.absolute()), 'wb')
            fout.write(r.data)
            if is_zipfile(str(file_path.absolute())):
                zip_file = ZipFile(str(file_path.absolute()), 'r')
                zip_file.extractall(self.folder)
                zip_file.close()
                os.remove(str(file_path.absolute()))
            else:
                os.remove(str(file_path.absolute()))
                return 'not zipfile'
        else:
            return 'http error'
        return 'save ' + file_name + ' success'

if __name__ == '__main__':
    fut = fut_data('/home/vodo/trader/history/')
    for i in range(30):
        print(fut.past_day(i))
