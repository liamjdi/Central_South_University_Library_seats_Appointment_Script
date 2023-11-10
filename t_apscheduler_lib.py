#File:t_apscheduler_lib.py
# MY MOTTO: 少时须知凌云志,曾许人间第一流.
# By: Liam-Jdi
# Time:3/29/2023 2:30 PM
# QQ-Mail:3161796832@qq.com
#说明：这个文件是用来定时执行t_datetime脚本的

import os
from apscheduler.schedulers.blocking import BlockingScheduler


def execute():
    os.system('python t_datetime.py')

scheduler = BlockingScheduler()
#每天的早上6：00:01准时执行预约
scheduler.add_job(execute,'cron',hour=6,minute=0,second=1)  
scheduler.start()
