# coding=utf-8
import config
import telebot
import threading
from bstry2 import anime_ser, anime_mov, movies, games, get_news
from db import add_user, get_user, update_, check_user
from telebot import types
import time
from checker import check_link

themes = {'animeser': anime_ser, 'animemov': anime_mov, 'movies': movies, 'games': games}


class my_bot(telebot.TeleBot):
    def scheduled(self):
        while True:
            anime_ser_new_link = check_link('animeser')
            if anime_ser_new_link and len(get_user('animeser')) != 0:
                a = list(map(lambda x: x[0], get_user('animeser')))
                for i in a:
                    send_writable_mes(i, get_news(anime_ser_new_link))
            anime_ser_new_link = check_link('animemov')
            if anime_ser_new_link and len(get_user('animemov')) != 0:
                a = list(map(lambda x: x[0], get_user('animemov')))
                for i in a:
                    send_writable_mes(i, get_news(anime_ser_new_link))
            anime_ser_new_link = check_link('movies')
            if anime_ser_new_link and len(get_user('movies')) != 0:
                a = list(map(lambda x: x[0], get_user('movies')))
                for i in a:
                    send_writable_mes(i, get_news(anime_ser_new_link))
            anime_ser_new_link = check_link('games')
            if anime_ser_new_link and len(get_user('games')) != 0:
                a = list(map(lambda x: x[0], get_user('games')))
                for i in a:
                    send_writable_mes(i, get_news(anime_ser_new_link))
            time.sleep(config.check_period)

    def start_action(self):
        thread = threading.Thread(target=self.scheduled)
        thread.start()


bot = my_bot(token=config.TOKEN, threaded=False)


def send_writable_mes(chatid, i):
    bot.send_message(chatid, '__*' + i['name'] + '*__', parse_mode="Markdown")
    tx = ''
    for j in i['text']:
        if str(j) != '':
            tx += j + '\n'
    bot.send_message(chatid, tx)
    if i['pic'] != '':
        pic = i['pic']
        if 'https://kg-portal' not in pic:
            pic = 'https://kg-portal.ru' + pic
        bot.send_message(chatid, pic)


def send_last_news(chatid, name):
    bot.send_message(chatid, 'Подождите пару секунд')
    anm = themes[name]()[::-1]
    anm = anm[-config.news_quantity:]
    for i in anm:
        send_writable_mes(chatid, i)


@bot.message_handler(commands=['start'])
def startpg(message):
    add_user(message.chat.id)
    startmenu = types.ReplyKeyboardMarkup(True, False)
    startmenu.row('Увидеть последние новости')
    startmenu.row('Подписаться на рассылку')
    startmenu.row('Отказаться от подписки')
    bot.send_message(message.chat.id, 'Привет!', reply_markup=startmenu)


@bot.message_handler(content_types=['text'])
def osnov(message):
    if message.chat.type == 'private':
        if message.text == 'Увидеть последние новости':
            markup = types.InlineKeyboardMarkup(row_width=2)
            theme1 = types.InlineKeyboardButton('Аниме сериалы', callback_data='print_animeser')
            theme2 = types.InlineKeyboardButton('Аниме фильмы', callback_data='print_animemov')
            theme3 = types.InlineKeyboardButton('Фильмы', callback_data='print_movies')
            theme4 = types.InlineKeyboardButton('Игры', callback_data='print_games')
            markup.add(theme1, theme2, theme3, theme4)
            bot.send_message(message.chat.id, 'Какую тематику хотите посмотреть?', reply_markup=markup)
        elif message.text == 'Подписаться на рассылку':
            markup = types.InlineKeyboardMarkup(row_width=2)
            theme1 = types.InlineKeyboardButton('Аниме сериалы', callback_data='sub_animeser')
            theme2 = types.InlineKeyboardButton('Аниме фильмы', callback_data='sub_animemov')
            theme3 = types.InlineKeyboardButton('Фильмы', callback_data='sub_movies')
            theme4 = types.InlineKeyboardButton('Игры', callback_data='sub_games')
            markup.add(theme1, theme2, theme3, theme4)
            bot.send_message(message.chat.id, 'На какую рассылку желаете подписаться?', reply_markup=markup)
        elif message.text == 'Отказаться от подписки':
            markup = types.InlineKeyboardMarkup(row_width=2)
            theme1 = types.InlineKeyboardButton('Аниме сериалы', callback_data='unsub_animeser')
            theme2 = types.InlineKeyboardButton('Аниме фильмы', callback_data='unsub_animemov')
            theme3 = types.InlineKeyboardButton('Фильмы', callback_data='unsub_movies')
            theme4 = types.InlineKeyboardButton('Игры', callback_data='unsub_games')
            markup.add(theme1, theme2, theme3, theme4)
            bot.send_message(message.chat.id, 'От какой рассылки желаете отписаться?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'print_animeser':
                send_last_news(call.message.chat.id, 'animeser')
            elif call.data == 'print_animemov':
                send_last_news(call.message.chat.id, 'animemov')
            elif call.data == 'print_movies':
                send_last_news(call.message.chat.id, 'movies')
            elif call.data == 'print_games':
                send_last_news(call.message.chat.id, 'games')
            elif call.data == 'sub_animeser':
                if check_user(call.message.chat.id, 'animeser'):
                    bot.send_message(call.message.chat.id, 'Вы уже подписаны на этот раздел!')
                else:
                    update_(call.message.chat.id, 'animeser', True)
                    bot.send_message(call.message.chat.id, 'Вы успешно подписались на этот раздел!')
            elif call.data == 'sub_animemov':
                if check_user(call.message.chat.id, 'animemov'):
                    bot.send_message(call.message.chat.id, 'Вы уже подписаны на этот раздел!')
                else:
                    update_(call.message.chat.id, 'animemov', True)
                    bot.send_message(call.message.chat.id, 'Вы успешно подписались на этот раздел!')
            elif call.data == 'sub_movies':
                if check_user(call.message.chat.id, 'movies'):
                    bot.send_message(call.message.chat.id, 'Вы уже подписаны на этот раздел!')
                else:
                    update_(call.message.chat.id, 'movies', True)
                    bot.send_message(call.message.chat.id, 'Вы успешно подписались на этот раздел!')
            elif call.data == 'sub_games':
                if check_user(call.message.chat.id, 'games'):
                    bot.send_message(call.message.chat.id, 'Вы уже подписаны на этот раздел!')
                else:
                    update_(call.message.chat.id, 'games', True)
                    bot.send_message(call.message.chat.id, 'Вы успешно подписались на этот раздел!')
            elif call.data == 'unsub_animeser':
                if not check_user(call.message.chat.id, 'animeser'):
                    bot.send_message(call.message.chat.id, 'Вы ещё не подписались на этот раздел!')
                else:
                    update_(call.message.chat.id, 'animeser', False)
                    bot.send_message(call.message.chat.id, 'Вы успешно отписались от этого раздела!')
            elif call.data == 'unsub_animemov':
                if not check_user(call.message.chat.id, 'animemov'):
                    bot.send_message(call.message.chat.id, 'Вы ещё не подписались на этот раздел!')
                else:
                    update_(call.message.chat.id, 'animemov', False)
                    bot.send_message(call.message.chat.id, 'Вы успешно отписались от этого раздела!')
            elif call.data == 'unsub_movies':
                if not check_user(call.message.chat.id, 'movies'):
                    bot.send_message(call.message.chat.id, 'Вы ещё не подписались на этот раздел!')
                else:
                    update_(call.message.chat.id, 'movies', False)
                    bot.send_message(call.message.chat.id, 'Вы успешно отписались от этого раздела!')
            elif call.data == 'unsub_games':
                if not check_user(call.message.chat.id, 'games'):
                    bot.send_message(call.message.chat.id, 'Вы ещё не подписались на этот раздел!')
                else:
                    update_(call.message.chat.id, 'games', False)
                    bot.send_message(call.message.chat.id, 'Вы успешно отписались от этого раздела!')
    except Exception as e:
        print(repr(e))


if __name__ == '__main__':
    bot.start_action()
    bot.polling(none_stop=True)
