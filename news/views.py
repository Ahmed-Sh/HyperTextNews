import itertools
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
import os
import json
from datetime import datetime


'''
# 1st way of sorting:
    sorted_news = sorted(my_news, key=lambda i: i['created'], reverse=True)
    grouped_news = itertools.groupby(sorted_news, lambda i: i['created'][:10])
'''
'''
# If you have a dictionary of the news and need to organize by key date, do the following:
all_news = OrderedDict(sorted(group_dates.items(), key=lambda x: datetime.strptime(x[0], '%Y-%m-%d'), reverse=True))
This basically:
1. Takes tuple 'group_dates.items()'.
2. Sort elements by key with applied function.
3. Parameter reverse is true for descending ordering.
4. sorted() returns a list of tuples like this [(key, value), (key, value)].
5. OrderedDict converts the list of tuples to a special type of dictionary that is the 
    same as usual dictionary but it maintains the orders of keys as inserted.
'''
'''
# another way
For those confused on how to sort and group the news:-
ALL_NEWS.sort(key=lambda x: datetime.strptime(x['created'], "%Y-%m-%d %H:%M:%S"), reverse=True)
def simple_date_fun(date):
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
all_news = [{'date': date, 'values': list(news)} for date, news in
                itertools.groupby(ALL_NEWS, lambda x: simple_date_fun(x['created']))]
'''

file_path = os.path.dirname(os.path.abspath(__file__))

'''
def reading_json():
    with open(file_path + "\\" + "news.json", "r")as f:
        my_news = json.load(f)
        sorted_news = sorted(my_news, key=lambda i: i['created'], reverse=True)
        grouped_news = itertools.groupby(sorted_news, lambda i: i['created'][:10])

    dates = []
    for k, v in grouped_news:
        dates.append(k)
    return my_news, dates
'''


def create_news(title, text):
    """Created new article and storage is JSON file"""

    with open(file_path + "\\" + "news.json", "r")as f:
        my_news = json.load(f)

    with open(file_path + "\\" + "news.json", "w")as f:
        news_item = {
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'text': text,
            'title': title,
            'link': int(datetime.timestamp(datetime.now()) * 1000),
        }
        my_news.append(news_item)
        json.dump(my_news, f)


def get_news(search=None):
    """If search parameters are passed, it searches for them,
    otherwise returns all results"""
    with open(file_path + "\\" + "news.json", "r")as f:
        news: list = json.load(f)
        news.sort(key=lambda x: x['created'], reverse=True)
        context = {}
        for article in news:
            date = article['created'].split()[0]
            if search:
                if search.lower() in article['title'].lower():
                    context.setdefault(date, []).append(article)
            else:
                context.setdefault(date, []).append(article)

        return context


class ComingSoon(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class MainPage(View):
    def get(self, request, *args, **kwargs):

        if request.GET:
            # If search parameters are passed, it searches for them
            # If search parameters are passed, it searches for them
            news = get_news(request.GET.get('q'))
        else:
            # If search parameters are not passed returns all news
            news = get_news()
        context = {'news': news}
        return render(request, "news/base.html", context=context)


class MyNews(View):
    def get(self, request, link, *args, **kwargs):
        with open(file_path + "\\" + "news.json", "r")as f:
            my_news = json.load(f)
        context = {"my_news": my_news, "link": int(link)}
        return render(request, "news/index.html", context=context)


class NewsCreatePage(View):
    """Create News view"""

    def get(self, request):
        return render(request, 'news/create.html')


    def post(self, request):
        title = request.POST.get('title')
        text = request.POST.get('text')
        create_news(title, text)
        return redirect('/news/')
