from datetime import date, timedelta
import urllib.request

class fut_data:
    def __init__(self, data_location):
        self.url = 'http://www.taifex.com.tw/DailyDownload/DailyDownloadCSV/Daily_'
        self.today = date.today()
        self.folder = data_location
    def get_today(self):
        file_name = self.today.strftime('%Y_%0m_%0d') + '.zip'
        if self.today.isoweekday() not in [6, 7]:
            urllib.request.urlretrieve(self.url + file_name, self.folder + file_name)
        else:
            print('is weekend')

if __name__ == '__main__':
    fut = fut_data('/home/vodo/trader/history/')
    fut.get_today()
