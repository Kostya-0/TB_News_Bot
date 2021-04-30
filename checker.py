from bstry2 import anime_ser, anime_mov, movies, games
from config import news_quantity

themes = {'animeser': anime_ser, 'animemov': anime_mov, 'movies': movies, 'games': games}


def check_link(name):
    with open(name + '.txt') as file:
        links_from_file = list(map(lambda x: x.strip('\n'), file.readlines()))
    links = list(filter(lambda x: x, themes[name](True)))[:news_quantity]
    if len(links_from_file) < len(links):
        with open(name + '.txt', 'w') as file:
            file.writelines('\n'.join(links))
        return links[0]
    elif links_from_file != links:
        with open(name + '.txt', 'w') as file:
            file.writelines('\n'.join(links))
        return links[0]
    else:
        return None


if __name__ == '__main__':
    check_link('animeser')
    check_link('animemov')
    check_link('movies')
    check_link('games')
