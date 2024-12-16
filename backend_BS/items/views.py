from django.shortcuts import render
from django.http import JsonResponse
from .models import Item, PriceHistory, PriceImg
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pickle
import time
import json
import random
from .models import SavedItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings


def item_price_history(request, item_id):
    price_history = PriceHistory.objects.filter(item_id=item_id).order_by('-date')
    history_data = [{'date': record.date, 'price': record.price} for record in price_history]
    return JsonResponse(history_data, safe=False)

def fetch_taobao_items(keyword):
    options = webdriver.ChromeOptions()
    service = Service(executable_path="/home/xijinping/chromedriver-linux64/chromedriver")
    options.add_argument("--disable-blink-features=AutomationControlled")
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
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)

    # 等待搜索结果加载
    time.sleep(20)

    # 获取商品信息
    items = []
    products = driver.find_elements(By.CSS_SELECTOR, '.gl-item')
    for product in products:
        title = product.find_element(By.CSS_SELECTOR, '.p-name a em').text
        price_text = product.find_element(By.CSS_SELECTOR, '.p-price').text.split('\n')[0]
        price = float(price_text.replace('￥', '').replace(',', ''))
        image = product.find_element(By.CSS_SELECTOR, '.p-img img').get_attribute('src')
        link = product.find_element(By.CSS_SELECTOR, '.p-name a').get_attribute('href')
        items.append({'name': title, 'price': price, 'image': image, 'link': link})

    driver.quit()
    return items

def search_items(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    if 'keywords' not in request.GET:
        return JsonResponse({'error': 'Missing keywords'}, status=401)
    keyword = request.GET.get('keywords', '')
    taobao_items = fetch_taobao_items(keyword)
    for taobao_item in taobao_items:
        Item.objects.update_or_create(
            name=taobao_item['name'],
            defaults={'price': taobao_item['price'], 'image': taobao_item['image'], 'link': taobao_item['link']}
        )
    keywords = keyword.split()
    items = Item.objects.filter(name__icontains=keywords[0])
    for kw in keywords[1:]:
        items = items & Item.objects.filter(name__icontains=kw)
    items_data = [{ 'name': item.name,  'image': item.image,  'link': item.link, 'price': item.price} for item in items]
    return JsonResponse(items_data, safe=False, content_type='application/json')

def save_item(request):
        if request.method != 'POST':
            return JsonResponse({'error': 'Invalid request method'}, status=400)
        
        data = json.loads(request.body)
        item_name = data.get('item_name')
        user_name = request.user
        if not item_name:
            return JsonResponse({'error': 'Missing item_name'}, status=401)
        
        try:
            item = Item.objects.get(name=item_name)
        except Item.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)
        SavedItem.objects.create(user=user_name, item=item)
        PriceHistory.objects.create(item=item, price=item.price, link=item.link, date=time.strftime('%Y-%m-%d %H:%M:%S'))
        
        return JsonResponse({'message': 'Item saved successfully'}, status=200)
def random_items(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    items = list(Item.objects.all())
    random_items = random.sample(items, min(len(items), 8))
    items_data = [{'name': item.name, 'image': item.image, 'link': item.link, 'price': item.price} for item in random_items]
    return JsonResponse(items_data, safe=False, content_type='application/json', status=200)

def get_price(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    data = json.loads(request.body)
    item_name = data.get('name')
    if not item_name:
        return JsonResponse({'error': 'Missing link'}, status=402)
    
    try:
        item = Item.objects.get(name=item_name)
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    
    options = webdriver.ChromeOptions()
    service = Service(executable_path="/home/xijinping/chromedriver-linux64/chromedriver")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options, service=service)

    driver.get("http://www.hisprice.cn/")

    # Wait for the page to load
    time.sleep(3)

    # Find the input box and enter the product URL
    search_box = driver.find_element(By.ID, 'kValId')
    search_box.clear()
    search_box.send_keys(item.link)
    search_box.send_keys(Keys.RETURN)

    # Wait for the results to load
    time.sleep(11)

    # Extract the latest price from the tooltip
    tooltip = driver.find_element(By.ID, 'Acontainertooltip')
    latest_price_text = tooltip.text
    latest_price = float(latest_price_text.replace(',', ''))

    # Close the WebDriver
    driver.quit()

    # Update the item's price and save to PriceHistory
    item.price = latest_price
    item.save()
    PriceHistory.objects.create(item=item, price=latest_price, date=time.strftime('%Y-%m-%d %H:%M:%S'))
    
    return JsonResponse({'message': 'Price updated successfully', 'latest_price': latest_price}, status=200)


def get_latest_saved_items(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=401)
    latest_prices = {}
    user = request.user
    saved_items = SavedItem.objects.filter(user=user)
    if not saved_items:
        return JsonResponse({'message': 'No saved items found for this user'}, status=404)
    
    item_ids = [saved_item.item.id for saved_item in saved_items]
    price_histories = PriceHistory.objects.raw('''
        SELECT *
        FROM items_pricehistory AS ph1
        WHERE ph1.item_id IN %s AND ph1.date = (
            SELECT MAX(date)
            FROM items_pricehistory AS ph2
            WHERE ph1.item_id = ph2.item_id
        )
    ''', [tuple(item_ids)])
    if not price_histories:
        return JsonResponse({'message': 'No saved items found'}, status=404)
    for history in price_histories:
        latest_prices[history.item_id] = {'name': history.item.name, 'latest_price': history.price}
    
    return JsonResponse(list(latest_prices.values()), safe=False, content_type='application/json', status=200)

def get_price_img(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    data = json.loads(request.body)
    item_link = data.get('link')
    if not item_link:
        return JsonResponse({'error': 'Missing link'}, status=401)
    
    try:
        item = Item.objects.get(link=item_link)
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    # Check if there is a price chart within the last 3 days
    screenshot_path = f"/home/xijinping/BS/BS_final/frontend/public/static/price_charts/{item.id}_price_chart.png"
    front_path = f"/static/price_charts/{item.id}_price_chart.png"
    three_days_ago = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time() - 64 * 60 * 60))
    recent_price_img = PriceImg.objects.filter(item=item, date__gte=three_days_ago).first()
    if recent_price_img:
        return JsonResponse({'message': 'Price chart saved successfully', 'price_chart': front_path}, status=200)
    options = webdriver.ChromeOptions()
    service = Service(executable_path="/home/xijinping/chromedriver-linux64/chromedriver")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # 设置 WebDriver
    driver = webdriver.Chrome(options=options, service=service)
    # Open the website
    driver.get("http://www.hisprice.cn/")

    # Wait for the page to load
    time.sleep(3)

    # Find the input box and enter the product URL
    search_box = driver.find_element(By.ID, 'kValId')
    search_box.clear()
    search_box.send_keys(item_link)
    search_box.send_keys(Keys.RETURN)

    # Wait for the results to load
    time.sleep(11)

    # Extract the historical prices from the chart
    canvas = driver.find_element(By.CLASS_NAME, "flot-overlay")
    driver.execute_script("arguments[0].scrollIntoView(true);", canvas)
    time.sleep(2)  # Wait for the canvas to be fully visible

    # Take a screenshot of the canvas
    canvas.screenshot(screenshot_path)

    # Close the WebDriver
    driver.quit()

    # Save the screenshot path to the item
    PriceImg.objects.create(item=item, image=screenshot_path)
    front_path = f"/static/price_charts/{item.id}_price_chart.png"
    return JsonResponse({'message': 'Price chart saved successfully', 'price_chart': front_path, 'item_id': item.id}, status=200)

def send_email(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    data = json.loads(request.body)
    subject = data.get('subject')
    message = data.get('message')
    recipient = data.get('recipient')
    
    if not subject or not message or not recipient:
        return JsonResponse({'error': 'Missing subject, message, or recipient'}, status=401)
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
        )
        return JsonResponse({'message': 'Email sent successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)