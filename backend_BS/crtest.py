from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# 这个路径要改成你下载的的chromedriver的存放地址
service = Service(executable_path="/home/xijinping/chromedriver-linux64/chromedriver")
driver = webdriver.Chrome(options=options, service=service)

driver.get("https://taobao.com")

