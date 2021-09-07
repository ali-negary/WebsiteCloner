from django.shortcuts import render
from urllib.parse import quote
from bs4 import BeautifulSoup
import requests

from . import models

# craigslist
base_website_url = 'https://losangeles.craigslist.org/d/services/search?query={}&sort=rel'
base_image_url = 'https://images.craigslist.org/{}_300x300.jpg'
image_not_found_url = 'data:image/png;base64,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'

# digikala.com
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
        post_image_ids = post.find(class_='result-image').get('data-ids')
        if post_image_ids:
            # this only extracts the first image.
            post_image = post_image_ids.split(',')[0].split(':')[1]
            post_image_url = base_image_url.format(quote(post_image))
        else:
            # an image saying no image found
            post_image_url = image_not_found_url

        results.append((post_title, post_url, post_price, post_image_url))

    material_for_front = {
        'search': search,
        'search_results': results,
    }
    return render(request, 'myApp/new_search.html', material_for_front)
