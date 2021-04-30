from bs4 import BeautifulSoup
import requests
from config import news_quantity


def get_news(link):
    resp1 = requests.get(link)
    soup1 = BeautifulSoup(resp1.text, 'lxml')
    a = {'name': '', 'text': '', 'pic': ''}
    a['name'] = soup1.find('h1', class_='news_title').text
    text_a = soup1.find('div', class_='news_text').find_all('p')
    for ii in range(len(text_a)):
        text_a[ii] = text_a[ii].text
    a['text'] = text_a
    try:
        a['pic'] = soup1.find('div', class_='news_text').find('picture').find('img').get('src')
    except AttributeError:
        a['pic'] = ''
    return a


def anime_ser(get_links=False):
    k = 0
    resp = requests.get('https://kg-portal.ru/news/anime/')
    soup = BeautifulSoup(resp.text, 'lxml')
    links = soup.find_all('div', class_="news_box anime_cat")
    for i in range(len(links)):
        if links[i].find('li', class_='tab donate'):
            links[i] = None
            continue
        links[i] = links[i].find('div', class_='news_output clearfix').find('div', class_="container").find(
            'input').get('value')
    if get_links:
        return links
    news = []
    for i in links:
        if i:
            k += 1
            news.append(get_news(i))
            if k >= news_quantity:
                return news
    return news


def anime_mov(get_links=False):
    k = 0
    resp = requests.get('https://kg-portal.ru/news/anime/')
    soup = BeautifulSoup(resp.text, 'lxml')
    links = soup.find_all('div', class_="news_box movies_cat")
    for i in range(len(links)):
        if links[i].find('li', class_='tab donate'):
            links[i] = None
            continue
        links[i] = links[i].find('div', class_='news_output clearfix').find('div', class_="container").find(
            'input').get('value')
    if get_links:
        return links
    news = []
    for i in links:
        if i:
            k += 1
            news.append(get_news(i))
            if k >= news_quantity:
                return news
    return news


def movies(get_links=False):
    k = 0
    resp = requests.get('https://kg-portal.ru/news/movies/')
    soup = BeautifulSoup(resp.text, 'lxml')
    links = soup.find_all('div', class_="news_box movies_cat")
    for i in range(len(links)):
        if links[i].find('li', class_='tab donate'):
            links[i] = None
            continue
        links[i] = links[i].find('div', class_='news_output clearfix').find('div', class_="container").find(
            'input').get('value')
    if get_links:
        return links
    news = []
    for i in links:
        if i:
            k += 1
            news.append(get_news(i))
            if k >= news_quantity:
                return news
    return news


def games(get_links=False):
    k = 0
    resp = requests.get('https://kg-portal.ru/news/games/')
    soup = BeautifulSoup(resp.text, 'lxml')
    links = soup.find_all('div', class_="news_box games_cat")
    for i in range(len(links)):
        if links[i].find('li', class_='tab donate'):
            links[i] = None
            continue
        links[i] = links[i].find('div', class_='news_output clearfix').find('div', class_="container").find(
            'input').get('value')
    if get_links:
        return links
    news = []
    for i in links:
        if i:
            k += 1
            news.append(get_news(i))
            if k >= news_quantity:
                return news
    return news


if __name__ == '__main__':
    anime_ser()
