from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pickle
from bs4 import BeautifulSoup
import time
import pandas as pd

options = Options()
service = Service(executable_path="/home/xijinping/chromedriver-linux64/chromedriver")
options.add_argument("--disable-blink-features=AutomationControlled")

# 设置 WebDriver
driver = webdriver.Chrome(options=options, service=service)

# 打开淘宝网站
driver.get('https://www.taobao.com/')

# 等待页面加载完成
time.sleep(3)

# 加载之前保存的 cookies
with open('tb_cookies.pkl', 'rb') as f:
    cookies = pickle.load(f)
for cookie in cookies:
    driver.add_cookie(cookie)

# 刷新页面以应用 cookies
driver.refresh()

# 等待页面加载完成
time.sleep(3)

# 输入关键词并搜索
search_box = driver.find_element(By.ID, 'q')
search_box.send_keys('laptop')
search_box.send_keys(Keys.RETURN)

# 等待搜索结果加载
time.sleep(3)

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
# 将页面源代码保存到文件
with open('taobao_page_source.html', 'w', encoding='utf-8') as file:
    file.write(soup.prettify())
# 解析商品信息
# 解析商品信息并保存
items = soup.find_all('div', class_='tbpc-col search-content-col')

# 遍历每个商品容器，提取信息
for item in items:
    # 提取商品名称
    title = item.find('div', class_='title--qJ7Xg_90').find('span').get_text(strip=True)
    
    # 提取商品图片
    img = item.find('img', class_='mainPic--Ds3X7I8z')
    image_url = img['src'] if img else None
    
    # 提取商品价格
    price = item.find('span', class_='priceInt--yqqZMJ5a').get_text(strip=True) if item.find('span', class_='priceInt--yqqZMJ5a') else 'N/A'
    
    # 提取商品链接
    link = item.find('a', class_='doubleCardWrapperAdapt--mEcC7olq')['href'] if item.find('a', class_='doubleCardWrapperAdapt--mEcC7olq') else None
    
    # 打印提取的信息
    print(f"商品名称: {title}")
    print(f"商品图片URL: {image_url}")
    print(f"商品价格: ¥{price}")
    print(f"商品链接: {link}")
    print('---')
driver.quit()

