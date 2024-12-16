from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

options = Options()
service = Service(executable_path="/home/xijinping/chromedriver-linux64/chromedriver")
options.add_argument("--disable-blink-features=AutomationControlled")

# 设置 WebDriver
driver = webdriver.Chrome(options=options, service=service)
# Open the website
driver.get("http://www.hisprice.cn/")

# Wait for the page to load
time.sleep(3)

# Find the input box and enter the product URL
product_url = "http://item.jd.com/100004538398.html"
search_box = driver.find_element(By.ID, 'kValId')
search_box.clear()
search_box.send_keys(product_url)
search_box.send_keys(Keys.RETURN)

# Wait for the results to load
time.sleep(5)

# Extract the historical prices from the chart
canvas = driver.find_element(By.CLASS_NAME, "flot-overlay")
driver.execute_script("arguments[0].scrollIntoView(true);", canvas)
time.sleep(2)  # Wait for the canvas to be fully visible

# Take a screenshot of the canvas
canvas.screenshot("price_chart.png")

# Close the WebDriver
driver.quit()