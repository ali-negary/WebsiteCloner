from django.shortcuts import render
from urllib.parse import quote
from bs4 import BeautifulSoup
import requests

from . import models

base_website_url = 'https://losangeles.craigslist.org/d/services/search?query={}&sort=rel'
digi_base_url = 'https://www.digikala.com/search/?q={}'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    # this .get in search is not HTTP GET/POST methods. it is because result of request.POST is dictionary.
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    search_url = base_website_url.format(quote(search))
    response = requests.get(search_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_listings = soup.find_all('li', {'class': 'result-row'})

    results = list()
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        post_price_object = post.find(class_='result-price')
        if post_price_object:
            post_price = post_price_object.text
        else:
            post_price = 'Price Unavailable'
        results.append((post_title, post_url, post_price))

    material_for_front = {
        'search': search,
        'search_results': results,
    }
    return render(request, 'myApp/new_search.html', material_for_front)
