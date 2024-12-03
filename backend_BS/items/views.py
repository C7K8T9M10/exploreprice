from django.shortcuts import render
from django.http import JsonResponse
from .models import Item, PriceHistory
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import json


def item_price_history(request, item_id):
    price_history = PriceHistory.objects.filter(item_id=item_id).order_by('-date')
    history_data = [{'date': record.date, 'price': record.price} for record in price_history]
    return JsonResponse(history_data, safe=False)

def fetch_taobao_items(keyword):
    url = f"https://search.jd.com/Search?keyword={keyword}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = []
    for item in soup.select('.item'):
        name = item.select_one('.title').get_text(strip=True)
        price = item.select_one('.price').get_text(strip=True)
        image = item.select_one('.pic img')['src']
        items.append({'name': name, 'price': price, 'image': image})
    return items

def search_items(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    if 'keywords' not in request.GET:
        return JsonResponse({'error': 'Missing keywords'}, status=400)
    keyword = request.GET.get('keywords', '')
    taobao_items = fetch_taobao_items(keyword)
    for taobao_item in taobao_items:
        Item.objects.update_or_create(
            name=taobao_item['name'],
            defaults={'price': taobao_item['price'], 'image': taobao_item['image']}
        )
    items = Item.objects.filter(name__icontains=keyword)
    items_data = [{'category': item.category, 'name': item.name, 'barcode': item.barcode, 'image': item.image} for item in items]
    return JsonResponse(items_data, safe=False, content_type='application/json')
