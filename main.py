import logging
import os 
import random
import sys
import time
import urllib.request

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# # 添加log
# if not os.path.exists("log"):
#     os.makedirs("log")

# log_file_path = "log/{}.log".format(time.strftime("%Y-%m-%d"))
# fh = logging.FileHandler(filename=log_file_path, encoding="UTF-8")
# logging.basicConfig(
#     handlers=[fh], format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger("whatever")

# 在当前目录下创建用于存放图片的文件夹
path = os.path.join("pictures")
if not os.path.exists(path):
    os.makedirs(path)

# 配置chromedriver
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
options.add_argument('User-Agent=Mozilla/5.0 '
	'(Windows NT 10.0,  Win64,  x64,  rv:96.0) Gecko/20100101 Firefox/96.0 ')
options.add_argument("disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)

# 配置urllib
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

# 打开豆瓣提示用户登入
driver.get('https://www.douban.com/') 
input("【请在打开的标签页中输入账号密码！登录完毕后请按任意键跳转】")

# # 把你的cookie写在这里
# cookies = []
# for cookie in cookies:
#     driver.add_cookie(cookie)

# 跳转到用户豆瓣主页
driver.get("https://www.douban.com/mine")
time.sleep(3)

# 打印cookies
cookies = driver.get_cookies()
print(cookies)

# 跳转到用户豆瓣广播页地址
hp_url = driver.current_url.split('?')
status_url = hp_url[0] + "statuses?p="

count = 0

pages = input("你想从广播第一页下载到第几页？")

for i in range(1, pages):
	driver.get(status_url + str(i))

	# 寻找网页中的图片
	time.sleep(2)
	imgs = driver.find_elements(By.CLASS_NAME, "view-large")
	print(imgs)

	time.sleep(3)

	for img in imgs:
		try:
			save_as = os.path.join(path, str(count) + '.jpg')
			print(img.get_attribute('href'))		

			image_url = img.get_attribute('href')
			urllib.request.urlretrieve(image_url, save_as)
			count += 1
			time.sleep(3 + random.random())
		except:
			print(f'failed to save image on page {i}')
