from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pickle
import time
options = Options()
service = Service(executable_path="/home/xijinping/chromedriver-linux64/chromedriver")
options.add_argument("--disable-blink-features=AutomationControlled")
# 设置 WebDriver
driver = webdriver.Chrome(options=options, service=service)

driver.get('https://www.jd.com/')

# 加载之前保存的 cookies
with open('jd_cookies.pkl', 'rb') as f:
    cookies = pickle.load(f)
for cookie in cookies:
    driver.add_cookie(cookie)

# 刷新页面以应用 cookies
driver.refresh()

# 等待页面加载完成
time.sleep(3)
# 输入关键词并搜索
search_box = driver.find_element(By.ID, 'key')
search_box.send_keys('laptop')
search_box.send_keys(Keys.RETURN)

# 等待搜索结果加载
time.sleep(3)

# 获取商品信息
products = driver.find_elements(By.CSS_SELECTOR, '.gl-item')
for product in products:
    title = product.find_element(By.CSS_SELECTOR, '.p-name a em').text
    price = product.find_element(By.CSS_SELECTOR, '.p-price').text
    link = product.find_element(By.CSS_SELECTOR, '.p-name a').get_attribute('href')
    print(f'Title: {title}\nPrice: {price}\nLink: {link}\n')