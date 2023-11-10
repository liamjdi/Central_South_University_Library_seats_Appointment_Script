# !/usr/bin/python
#File:t_datetime.py
# -*- coding: UTF-8 -*-
# MY MOTTO: 少时须知凌云志,曾许人间第一流.
# By: Liam-Jdi
# Time:2023-10-15 20:08 PM（重构）
# QQ-Mail:3161796832@qq.com
# 说明：这个文件是预约图书馆的脚本(重构之后的了)

####！！！注意！！！###
#本次重构加入了一些功能，包括但不限于：
#1.在预约的同时以较高频率进行截图，后期整合成一个动图，以达到记录预约过程的效果。当然效果不是那么好，有同学有更好的做法欢迎和我交流。
#2.出错的时候会发送带有上述gif文件的邮件，当然这里也可以使用微信公众号推送，比如pushplus推送加就挺好用的
#####################


from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from datetime import timedelta
from selenium.webdriver.chrome.options import Options
import time
import os
import base64
import threading
from PIL import Image
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header


#图书馆登录认证的网址
CSU_LIB_login_url = "https://ca.csu.edu.cn/authserver/login?type=userNameLogin&service=http%3A%2F%2Flibzw.csu.edu.cn%2Fcas%2Findex.php%3Fcallback%3Dhttp%3A%2F%2Flibzw.csu.edu.cn%2Fhome%2Fweb%2Ff_second"
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
#账号和密码
username = "学号"
password = "密码"

#存储制作gif所需的png文件的临时目录
img_dir = 'img'
#这个结果用来表示是否约到了理想的座位,-1表示没约到，0表示有预约了已经，1表示约到了
book_result = -1


#清空path路径下的所有文件，如果不存在path路径就创建path路径
def clear_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)
    else:
        [os.remove(os.path.join(path, file_name)) for file_name in os.listdir(path)]

#清空img_dir路径下所有文件，并且不间断截图（线程执行）
def shot(dr,img_dir):
    i = 0
    clear_dir(img_dir)  # 清空目录
    while True:
        img_file = os.path.join(img_dir,f'{i}.png')
        try:
            dr.save_screenshot(img_file)
        except:
            return
        i+=1

#得到tomorrow_result和图书馆明天的segment
def get_tomorrowResult_and_segment():
    tomorrow_result = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    #这里，时间间隔加xxx是要你自己去尝试的。
    #【提示】http://libzw.csu.edu.cn/web/seat3?area=70&segment=1682935&day=2023-11-11&startTime=07:30&endTime=22:00
    #正如上面的网址所示，每天的segment和day都是变化的，所以说，你要知道下面的xxx是和你要预约的地方有关系的嗷
    segment = str((datetime.now() - datetime(2023, 1, 1, 5, 58)).days + xxx) 
    return tomorrow_result,segment

#进行登录认证
def csu_lib_login(username,password,CSU_LIB_login_url,browser):
    browser.get(CSU_LIB_login_url)
    browser.find_element(By.ID, "username").clear()
    browser.find_element(By.ID, "username").send_keys(username)
    browser.find_element(By.ID, "password").clear()
    browser.find_element(By.ID, "password").send_keys(password)
    browser.find_element(By.ID, "login_submit").click()

#输入参数时，分，秒，程序便会在不早于当天的这个时段执行
def do_later_than(hour=6,minute=0,second=1):
    current_time = datetime.now()
    execute_time = current_time.replace(hour=hour,minute=minute,second=second)
    #print(current_time,"  ",execute_time)
    if execute_time > current_time:
        time.sleep((execute_time - current_time).total_seconds())

#预约座位,约到了返回1，没约到返回-1，预约了其他座位返回0.这里的number需要自己去尝试，F12，因为这是个css选择器，很好找到的。
def book_seat(browser,number="XF7A001"):
    browser.find_element(By.CSS_SELECTOR, "li[data-data*='\"name\":\"{}\"']".format(number)).click() 
    time.sleep(0.5)
    choice = browser.find_elements(By.XPATH, "/html/body/div[11]/div/table/tbody/tr[3]/td/div[2]/button[2]")
    if len(choice) != 0:
        choice[0].click()
        time.sleep(0.5)
        choice2 = browser.find_elements(By.XPATH, "/html/body/div[11]/div/table/tbody/tr[3]/td/div[2]/button")
        if len(choice2) != 0:
            choice2[0].click()
            print("succ({})".format(number))
            return 1
        else:
            print("have booked other seates")
            return 0
    else:
        print("failed at {}".format(number))
        return -1

#主程序开始
print(time.strftime("\n%Y-%m-%d %H:%M:%S",time.localtime(int(time.time()))),"(The time begin to book)begin: ")

#下面启动浏览器，开始预约
print("start : ")
chromedriver = chrome_driver_binary
os.environ["webdriver.chrome.driver"] = chromedriver

browser = webdriver.Chrome(executable_path='/usr/local/Soft/Chrome/chromedriver', chrome_options=chrome_options)
browser.implicitly_wait(10)  # 等待十秒
try:
    #登录
    csu_lib_login(username,password,CSU_LIB_login_url,browser)
    
    tomorrow_result,segment = get_tomorrowResult_and_segment()
    do_later_than(6,0,5)
    
    t = threading.Thread(target=shot,args=(browser,img_dir))
    t.start()
    
    #下面网址自己找，如http://libzw.csu.edu.cn/web/seat3?area=70&segment=1682935&day=2023-11-11&startTime=07:30&endTime=22:00
    browser.get(
        'http://libzw.csu.edu.cn/web/seat3?area=70&segment=' + segment + '&day=' + tomorrow_result + '&startTime=07:30&endTime=22:00')  # 注意，这里的segment就是和日期有关的数
    #下面的choice 1~5是要自己填的嗷
    book_result = book_seat(browser,"choice 1")
    if book_result < 0:
        book_result = book_seat(browser,"choice 2")
        if book_result < 0:
            book_result = book_seat(browser,"choice 3")
            if book_result < 0:
                book_result = book_seat(browser,"choice 4")
                if book_result < 0:
                    book_result = book_seat(browser,"choice 5")

    if book_result == -1:
        raise Exception("tried xxx-xxx,but we failed")
              
except Exception as e:
    happen_exception = str(e)
    print(happen_exception)

    #处理截取图片生成gif
    img_list = os.listdir(img_dir)  # 列出目录所有图片
    img_list.sort(key=lambda x: int(x[:-4]))  # 排序
    first_img = Image.open(os.path.join(img_dir, img_list[0]))  # 第一张图片对象
    else_imgs = [Image.open(os.path.join(img_dir, img)) for img in img_list[1:]]  # 剩余图片对象
    first_img.save("record(tomorrow).gif", append_images=else_imgs,duration=800,save_all=True,loop=0) # 拼接保存

    #下面是发邮件的部分
    con = smtplib.SMTP_SSL('smtp.163.com', 465)
    con.login('xxxx@163.com', 'xxxx')#邮箱账号和密码，这里需要自己了解一下邮箱授权码相关的知识
    msg = MIMEMultipart()
    subject = Header("csu lib book failed","utf-8").encode()
    msg['Subject'] = subject
    msg['From'] = 'xxx@163.com <xxx@163.com>'
    msg['To'] = 'yyyy@qq.com,zzzz@qq.com'
    html = MIMEText(happen_exception, 'html', 'utf-8')
    msg.attach(html)
    #将.gif作为附件发送
    with open ("record(tomorrow).gif","rb") as file:
        attachment = MIMEApplication(file.read())
        attachment.add_header("Content-Disposition","inline",filename='bookProcessRecord.gif')
        msg.attach(attachment)
    
    con.sendmail('xxx@163.com', ['yyyy@qq.com', 'zzzz@qq.com'], msg.as_string())
    con.quit()


finally:
    print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(time.time()))),"(The time end to book)end: \n")
    browser.quit()
    #处理截取图片生成gif
    img_list = os.listdir(img_dir)  # 列出目录所有图片
    img_list.sort(key=lambda x: int(x[:-4]))  # 排序
    first_img = Image.open(os.path.join(img_dir, img_list[0]))  # 第一张图片对象
    else_imgs = [Image.open(os.path.join(img_dir, img)) for img in img_list[1:]]  # 剩余图片对象
    first_img.save("record(tomorrow).gif", append_images=else_imgs,duration=800,save_all=True,loop=0) # 拼接保存
    clear_dir(img_dir)
    
    
