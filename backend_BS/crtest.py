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

driver.get("https://baidu.com")
print(driver.title)

def search_jd(keyword):
    driver.get("https://www.jd.com")
    search_box = driver.find_element(By.ID, "key")
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # 等待页面加载

    items = driver.find_elements(By.CSS_SELECTOR, ".gl-item")
    results = []
    for item in items:
        title = item.find_element(By.CSS_SELECTOR, ".p-name em").text
        price = item.find_element(By.CSS_SELECTOR, ".p-price i").text
        link = item.find_element(By.CSS_SELECTOR, ".p-name a").get_attribute("href")
        results.append({"title": title, "price": price, "link": link})

    return results

def login_cookie():
    driver.get("https://passport.jd.com/new/login.aspx")
    driver.maximize_window()
    time.sleep(2)
    
    # Switch to QR code login
    driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/div/div[3]/a').click()
    time.sleep(10)  # Wait for manual QR code scanning
    
    # Verify login success
    if "我的京东" in driver.page_source or "退出" in driver.page_source:
        print("Login successful")
        # Get cookies
        my_cookie = driver.get_cookies()
        data_cookie = json.dumps(my_cookie)
        with open("jd_cookies", "w") as fp:
            fp.write(data_cookie)
    else:
        print("Login failed")

def get_url_with_cookies(url):
    driver.get("https://www.jd.com")
    driver.delete_all_cookies()
    
    with open("jd_cookies", "r") as fp:
        jd_cookies = fp.read()
    
    jd_cookies_dict = json.loads(jd_cookies)
    for cookie in jd_cookies_dict:
        # Ensure the domain of the cookie matches the current domain
        if 'domain' in cookie:
            del cookie['domain']
        driver.add_cookie(cookie)
    
    driver.get(url)
    assert '退出' in driver.page_source
    print(url)

keyword = "laptop"

login_cookie()
get_url_with_cookies("https://www.jd.com")
products = search_jd(keyword)
for product in products:
    print(product)

driver.quit()
