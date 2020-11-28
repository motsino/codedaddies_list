import re
from django.db import models
import requests
from django.shortcuts import render
from django.views.generic import *
from requests.utils import requote_uri
import bs4
from . import models

BASE_SITE_URL = 'https://olist.ng/filter?keyword={}'


# Create your views here.
class HomeView(TemplateView):
    template_name = 'base.html'


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_SITE_URL.format(requote_uri(search))
    print(final_url)
    response = requests.get(final_url)
    data = response.text

    soup = bs4.BeautifulSoup(data, features='html.parser')

    post_rows = soup.find_all('a', {'class': 'item'})

    post_url = post_rows[0].get('href')
    post_photo = post_rows[0].find(class_='photos')
    post_photo_info = post_photo.find(class_='premium').text
    post_photo_source = post_photo.find('img', {'src': re.compile('.jpg')}).get('src')
    post_content = post_rows[0].find(class_='content')
    post_desc = post_content.find(class_='content-body').text
    post_title = post_content.find(class_='title').text
    post_price = post_content.find(class_='price').text
    post_region = post_content.find(class_='regionMessage').text

    final_posts = []

    for post in post_rows:
        post_photo = post.find(class_='photos')
        if post_photo.find(class_='premium'):
            post_photo_info = post_photo.find(class_='premium')
        else:
            post_photo_info = ''
        post_photo_source = post_photo.find('img', {'src': re.compile('.jpg')}).get('src')
        post_url = post.get('href')
        post_content = post.find(class_='content')
        post_desc = post_content.find(class_='content-body').text
        post_title = post_content.find(class_='title').text
        if post_content.find(class_='price'):
            post_price = post_content.find(class_='price').text
        else:
            post_price = 'N/A'
        post_region = post_content.find(class_='regionMessage').text

        final_posts.append(
            (post_url, post_photo_info, post_photo_source, post_title, post_desc, post_price, post_region))
        # we have text-lighten,text-darken,text-accent in case we want to change the text's color and others
    # print(post_url)
    # print(post_photo_source)
    # print(post_region)
    # print(post_photo_info)

    stuff_for_frontend = {'search': search, 'final_posts': final_posts, }
    return render(request, 'my_app/new-search.html', stuff_for_frontend)
