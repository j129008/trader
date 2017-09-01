from crontab import CronTab
from datetime import time

trader_cron = CronTab(user=True)
job = trader_cron.new(command='/usr/bin/python3 /home/vodo/trader/trader.py > /tmp/cron.log 2>&1')
job.setall('45 8 * * 1-5')
job.set_comment('time to trade')

trader_cron.write()
