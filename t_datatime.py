# MY MOTTO: 少时须知凌云志,曾许人间第一流.
# By: Liam-Jdi
# Time:3/29/2023 2:35 PM
# QQ-Mail:3161796832@qq.com
# 说明：这个文件是预约图书馆的脚本，Linux平台下

from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from datetime import timedelta
from selenium.webdriver.chrome.options import Options
import time
import os
import base64

# 图书馆用户认证的路径,学校的身份认证又升级啦啦啦[登录教务系统等，只需要改成对应的认证网址就可以了]
#CSU_LIB_url = "https://ca.csu.edu.cn/authserver/login?service=http%3A%2F%2Flibzw.csu.edu.cn%2Fcas%2Findex.php%3Fcallback%3Dhttp%3A%2F%2Flibzw.csu.edu.cn%2Fhome%2Fweb%2Ff_second"
CSU_LIB_url = "https://ca.csu.edu.cn/authserver/login?type=userNameLogin&service=http%3A%2F%2Flibzw.csu.edu.cn%2Fcas%2Findex.php%3Fcallback%3Dhttp%3A%2F%2Flibzw.csu.edu.cn%2Fhome%2Fweb%2Ff_second"

# 浏览器路径和driver路径
binary_location = '/usr/bin/google-chrome'  # 浏览器位置
chrome_driver_binary = '/usr/local/Soft/Chrome/chromedriver'  # webdriver位置
chrome_options = Options()
chrome_options.binary_location = binary_location
# 下面添加启动参数
chrome_options.add_argument('--no-sandbox')  # 以最高权限运行，沙盒模式运行
chrome_options.add_argument('--headless')  # 无界面运行（无头模式）
chrome_options.add_argument('--disable-gpu')  # 禁用gpu
chrome_options.add_argument('--disable-dev-shm-usage')  # 大量渲染时写入/tmp
chrome_options.add_argument('--window-size=1960,1080')  # 浏览器窗口大小
chrome_options.add_argument(r'user-data-dir=/root/.config/google-chrome/')  # 加载用户配置文件。使用浏览器的数据目录，这样就不会每次登录都还要在不可信设备验证了

print(time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(int(time.time()))), " begin：")

################下面是预约###########################
print("yyy start:")
username = "xxxxxxxxxx"
password = "pppppppppp"

chromedriver = chrome_driver_binary
os.environ["webdriver.chrome.driver"] = chromedriver

browser = webdriver.Chrome(executable_path='/usr/local/Soft/Chrome/chromedriver', chrome_options=chrome_options)
browser.implicitly_wait(10)  # 等待十秒
try:
    
    # 打开网页
    browser.get(CSU_LIB_url)
    browser.find_element(By.ID, "username").clear()
    browser.find_element(By.ID, "username").send_keys(username)
    browser.find_element(By.ID, "password").clear()
    browser.find_element(By.ID, "password").send_keys(password)
    browser.find_element(By.ID, "login_submit").click()

    # 现在开始预约
    tomorrow_result = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    segment = str((datetime.now() - datetime(2023, 1, 1, 5, 58)).days + 11111)  # 这里，时间间隔加多少自己去试一下吧，和日期以及你要预约的哪个场馆有关。

    
    #6：00 start
    now_second = datetime.now().second
    while now_second >40:
        now_second = datetime.now().second
    time.sleep(0.5)
    #这里的url也是需要你自己去试出来的
    browser.get(
        'http://libzw.csu.edu.cn/web/seat33333?area=77777&segment=' + segment + '&day=' + tomorrow_result + '&startTime=07:30&endTime=22:00')  # 注意，这里的segment就是和日期有关的数

    browser.find_element(By.CSS_SELECTOR, "li[data-data*='\"name\":\"xxxx\"']").click()  # 这里用了css选择器,第一选择
    time.sleep(0.5)
    choice = browser.find_elements(By.XPATH, "/html/body/div[11]/div/table/tbody/tr[3]/td/div[2]/button[2]")
    if len(choice) != 0:#约上了
        choice[0].click()
        time.sleep(0.5)
        choice2 = browser.find_elements(By.XPATH, "/html/body/div[11]/div/table/tbody/tr[3]/td/div[2]/button")
        if len(choice2) != 0:
            choice2[0].click()
            print("succ(xxxx) ：")
        else:
            print("有其它预约")
            browser.get_screenshot_as_file(tomorrow_result + r"screen3.png")
    else:
        pass
    
finally:
    print(time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(int(time.time()))), " end . ")
    browser.quit()
