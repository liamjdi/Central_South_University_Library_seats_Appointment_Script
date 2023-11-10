
Here is the English translation of the content:

# Central South University Library Seat Booking System Webpage Version Early Morning 6 O'clock Scheduled Login Script Linux(server) python+selenium(without request)

# Preparations
1. You need a server, I chose Tencent Cloud. 
2. Download a handy SSH tool, I think MobaXterm is very handy as it provides SFTP for easy file modification.
3. Set up the python environment and download Google Chrome browser on the server, and install the corresponding chromedriver.

# Initial Login
Because the school has multi-factor authentication, some tricks are needed to achieve future logins with only the saved username and password. 

【Hint: Repeated, I did not use request, I tried it but it seemed more complicated, if anyone has succeeded please share with me】

```
#### Write at the beginning !!! This file is quite old, some modifications may be needed, as long as you can scan the QR code to log in, then future logins only need username and password to achieve automatic booking.

# MY MOTTO: Know the lofty ambition when time permits, once promised to be the best in the world.
# By: Liam-Jdi 
# Time: 5/12/2023 9:00 PM
# QQ-Mail: 3161796832@qq.com
# Description: This file is because the library (including academic affairs system, etc.) Added untrusted device verification, we need to scan the QR code for the initial login (when I tested, the SMS verification code could not be sent), there are a few things to note,
# Here chrome_options.add_argument(r'user-data-dir=/root/.config/google-chrome/') is to use the browser's data directory, so it will not require untrusted device verification every time after login. 
# Also, familiarise yourself with browser.get_screenshot_as_file(r"screen.png") to print the current interface to see which step,
# You can choose QQ or WeChat scan verification, but bind one number to one, release it promptly after use oh oh

# Selenium code to log in
```

# Writing the booking script
```
#!/usr/bin/python 
#File: t_datetime.py
# -*- coding: UTF-8 -*-
# MY MOTTO: Know the lofty ambition when time permits, once promised to be the best in the world.
# By: Liam-Jdi
# Time:2023-10-15 8:08 PM(Reconstruction)
# QQ-Mail: 3161796832@qq.com
# Description: This file is the script for booking the library (reconstructed)

#### !!! Notice !!! ###
# This reconstruction has added some functions, including but not limited to: 
# 1. Take screenshots at a relatively high frequency during booking and integrate them into a gif to record the booking process. Of course, the effect is not very good, and welcome suggestions from others.
# 2. If an error occurs, send an email with the gif file attached. Push notifications to WeChat official accounts can also be used.

# Selenium code for booking seat
```

# Writing the scheduled script
```
#File: t_apscheduler_lib.py
# MY MOTTO: Know the lofty ambition when time permits, once promised to be the best in the world. 
# By: Liam-Jdi
# Time:3/29/2023 2:30 PM
# QQ-Mail: 3161796832@qq.com
# Description: This file is used to schedule the execution of the t_datetime script

import os
from apscheduler.schedulers.blocking import BlockingScheduler


def execute():
    os.system('python t_datetime.py')

scheduler = BlockingScheduler()  
# Schedule precise execution at 6:00:01 every day
scheduler.add_job(execute,'cron',hour=6,minute=0,second=1)   
scheduler.start()
```


# Execution
Okay, now to the exciting moment. Use nohup to run it in the background:

```
## Create background task
$ nohup python t_apscheduler.py > zndxtsg.log 2>&1 & 

## Check tasks  
$ ps -aux | grep "t_apscheduler.py"

## Delete task
$ kill -9 xxx

# Closing Words
When I started writing the code it was March, and now it's November, so over the past 7-8 months the script has gradually become more stable. As I'm doing postgraduate studies now I no longer need this system, so this experience has been quite valuable.
```
